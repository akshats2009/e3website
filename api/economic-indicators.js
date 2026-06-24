const START_YEAR = 2000;

const SERIES_CONFIG = {
  cpi: { id: "CPIAUCSL" },
  core_cpi: { id: "CPILFESL" },
  ppi: { id: "PPIACO" },
  core_pce: { id: "PCEPILFE" },
  fed_funds: { id: "FEDFUNDS" },
  unemployment: { id: "UNRATE" },
  payrolls: { id: "PAYEMS", transform: (value) => value / 1000 }, // thousands -> millions
  ten_year: { id: "GS10" },
};

function buildYearRange(start, end) {
  const years = [];
  for (let year = start; year <= end; year += 1) {
    years.push(year);
  }
  return years;
}

function interpolateSeries(years, valuesByYear) {
  const knownYears = Object.keys(valuesByYear)
    .map(Number)
    .filter((year) => Number.isFinite(year))
    .sort((a, b) => a - b);

  if (!knownYears.length) {
    return years.map(() => 0);
  }

  return years.map((year) => {
    const exact = valuesByYear[year];
    if (typeof exact === "number" && Number.isFinite(exact)) {
      return exact;
    }

    let previous = null;
    let next = null;
    for (let i = 0; i < knownYears.length; i += 1) {
      const current = knownYears[i];
      if (current < year) previous = current;
      if (current > year) {
        next = current;
        break;
      }
    }

    if (previous == null && next == null) return 0;
    if (previous == null) return valuesByYear[next];
    if (next == null) return valuesByYear[previous];

    const ratio = (year - previous) / (next - previous);
    return valuesByYear[previous] + (valuesByYear[next] - valuesByYear[previous]) * ratio;
  });
}

function parseFredCsv(csvText, transform) {
  const lines = String(csvText || "").trim().split(/\r?\n/);
  const byYear = {};
  let lastDate = null;

  for (let i = 1; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line) continue;

    const commaIndex = line.indexOf(",");
    if (commaIndex < 0) continue;

    const dateStr = line.slice(0, commaIndex).trim();
    const valueStr = line.slice(commaIndex + 1).trim();
    if (!dateStr || valueStr === "." || valueStr === "") continue;

    const value = Number(valueStr);
    if (!Number.isFinite(value)) continue;

    const year = Number(dateStr.slice(0, 4));
    if (!Number.isFinite(year) || year < START_YEAR) continue;

    const normalized = typeof transform === "function" ? transform(value) : value;
    if (!Number.isFinite(normalized)) continue;

    if (!byYear[year]) {
      byYear[year] = { sum: 0, count: 0 };
    }
    byYear[year].sum += normalized;
    byYear[year].count += 1;
    lastDate = dateStr;
  }

  const averagedByYear = {};
  Object.keys(byYear).forEach((key) => {
    const bucket = byYear[key];
    if (!bucket || !bucket.count) return;
    const year = Number(key);
    averagedByYear[year] = bucket.sum / bucket.count;
  });

  return { averagedByYear, lastDate };
}

async function fetchFredSeries(seriesId) {
  const url = `https://fred.stlouisfed.org/graph/fredgraph.csv?id=${seriesId}`;
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed ${seriesId} (${response.status})`);
  }
  return response.text();
}

module.exports = async function handler(req, res) {
  try {
    const entries = Object.entries(SERIES_CONFIG);
    const settled = await Promise.allSettled(
      entries.map(async ([key, cfg]) => {
        const csv = await fetchFredSeries(cfg.id);
        const parsed = parseFredCsv(csv, cfg.transform);
        return [key, parsed];
      })
    );

    const validSeries = {};
    let maxObservedYear = START_YEAR;
    let asOfDate = null;

    settled.forEach((result) => {
      if (result.status !== "fulfilled") return;

      const [key, parsed] = result.value;
      const yearKeys = Object.keys(parsed.averagedByYear).map(Number);
      if (!yearKeys.length) return;

      maxObservedYear = Math.max(maxObservedYear, Math.max.apply(null, yearKeys));
      if (!asOfDate || (parsed.lastDate && parsed.lastDate > asOfDate)) {
        asOfDate = parsed.lastDate || asOfDate;
      }
      validSeries[key] = parsed.averagedByYear;
    });

    const seriesKeys = Object.keys(validSeries);
    if (!seriesKeys.length) {
      throw new Error("No indicator series fetched");
    }

    const endYear = Math.max(new Date().getUTCFullYear(), maxObservedYear);
    const years = buildYearRange(START_YEAR, endYear);
    const series = {};

    seriesKeys.forEach((key) => {
      series[key] = interpolateSeries(years, validSeries[key]).map((value) =>
        Number(value.toFixed(4))
      );
    });

    res.setHeader("Cache-Control", "s-maxage=21600, stale-while-revalidate=43200");
    res.status(200).json({
      source: "FRED",
      generatedAt: new Date().toISOString(),
      asOfDate,
      years,
      series,
      partial: seriesKeys.length < entries.length,
    });
  } catch (error) {
    res.status(500).json({
      error: "Unable to fetch live indicator data",
      detail: error && error.message ? error.message : "Unknown error",
    });
  }
};
