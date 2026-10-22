# Article content. Mini-markdown: "## " h2, "### " h3, "- " bullets, "1. " numbered, "| " tables, "> " callout.
# {R} = relative path to site root.
ARTICLES = [
dict(slug="seeding-rate-corn-soybeans", cat="Planting", title="How to Calculate Seeding Rate for Corn and Soybeans",
 desc="Learn the seeding rate formula, how germination and emergence change it, and how to convert seeds per acre into bags and cost.",
 tools=["seed-rate-calculator","crop-profit-calculator"], related=["crop-rotation-basics","crop-budget-break-even-guide","soil-testing-and-ph-guide"],
 sources=[("USDA Natural Resources Conservation Service","https://www.nrcs.usda.gov"),("USDA National Agricultural Statistics Service","https://www.nass.usda.gov")],
 body="""
Seeding rate is the number of seeds you put in the ground per acre. Plant too few and you leave yield on the table; plant too many and you pay for seed that never pays you back. The right number comes from a simple formula that starts with the stand you want at harvest.

## The seeding rate formula
Work backward from your target final plant population:

> **Seeds per acre = Target plants per acre ÷ (Germination % × Emergence %)**

Germination comes from the seed tag. Emergence (also called field survival) accounts for seeds that germinate in the lab but never become healthy plants in your field. Many growers use 90 to 95 percent for good seedbeds and lower numbers for cold, wet or crusted soils.

**Example:** You want 34,000 corn plants per acre. The tag says 95% germination and you expect 92% emergence. 34,000 ÷ (0.95 × 0.92) = 34,000 ÷ 0.874 = about **38,900 seeds per acre**.

## Typical target populations
Targets depend on hybrid or variety, soil productivity, moisture and planting date, so treat these as starting points and confirm with your state land-grant university or seed dealer.

| Crop | Common target |
|---|---|
| Corn (grain) | 30,000 to 36,000 plants per acre |
| Soybeans | 100,000 to 140,000 seeds per acre planted |
| Winter wheat (drilled) | 1.0 to 1.5 million seeds per acre |

Corn on lower-yield or drought-prone ground often does better at the low end. High-yield, well-watered fields may justify more. Soybean yield response tends to flatten once you reach a moderate population, which is why economic trials often favor the lower half of the range when stands are uniform.

## Turn seeds per acre into bags and cost
Seed companies sell corn in units of about 80,000 kernels and soybeans in units of about 140,000 seeds, though bag sizes vary, so check your tag.

1. Multiply seeds per acre by acres to get total seeds.
2. Divide by seeds per bag and round up.
3. Multiply bags by price per bag.

For 100 acres at 38,900 seeds per acre, you need 3,890,000 seeds, or 48.6 bags of 80,000. Round up to **49 bags**.

## Check your actual stand
Count plants in a measured length of row, then convert to plants per acre. One thousandth of an acre in 30-inch rows is 17 feet 5 inches of row. Multiply the plants you count by 1,000 to estimate plants per acre. Do this in several spots so one thin patch does not mislead you.

## Common mistakes
- Using the same rate every year without checking the germination on the new seed lot.
- Skipping planter calibration, so the monitor says one thing and the field says another.
- Planting into cold, saturated soil and expecting normal emergence.
- Ignoring replant economics: a thinner stand is sometimes better kept than torn up.

Try the [Seed Rate Calculator]({R}tools/seed-rate-calculator.html) to run these numbers for your own acres and seed cost.
"""),
dict(slug="npk-fertilizer-labels-explained", cat="Fertility", title="NPK Fertilizer Labels Explained: How to Read and Calculate Rates",
 desc="What the three numbers on a fertilizer bag mean, how P2O5 and K2O convert to P and K, and how to turn a nutrient target into pounds of product.",
 tools=["fertilizer-calculator","crop-profit-calculator"], related=["soil-testing-and-ph-guide","crop-rotation-basics","seeding-rate-corn-soybeans"],
 sources=[("USDA NRCS Nutrient Management","https://www.nrcs.usda.gov"),("USDA Economic Research Service","https://www.ers.usda.gov")],
 body="""
Every fertilizer bag shows three numbers, such as 18-46-0. They are the **grade**: the percent by weight of nitrogen (N), phosphate (P2O5) and potash (K2O). A 50-pound bag of 10-10-10 holds 5 pounds each of N, P2O5 and K2O, with the remaining 35 pounds being carriers and filler.

## What the three numbers mean
- **N** is elemental nitrogen.
- **P2O5** is a way of reporting phosphorus. Actual elemental P is about 43.6% of the P2O5 number.
- **K2O** is a way of reporting potassium. Actual elemental K is about 83% of the K2O number.

Soil test labs and extension recommendations in the United States usually give P and K advice as pounds of P2O5 and K2O per acre, which makes the label math straightforward.

## Common fertilizer products
| Product | Typical grade | Notes |
|---|---|---|
| Urea | 46-0-0 | Dry; can lose N as ammonia if left on the surface |
| Ammonium nitrate | 34-0-0 | Dry; limited availability in some areas |
| Anhydrous ammonia | 82-0-0 | Gas stored under pressure; injected |
| UAN solution | 28-0-0 or 32-0-0 | Liquid; weight per gallon varies by grade |
| Ammonium sulfate | 21-0-0 | Also supplies about 24% sulfur |
| DAP | 18-46-0 | Supplies N and P2O5 |
| MAP | 11-52-0 | Supplies N and P2O5 |
| Potash (muriate) | 0-0-60 | Main K source |

## Convert a nutrient target into pounds of product
> **Pounds of product per acre = Pounds of nutrient needed ÷ (grade ÷ 100)**

**Nitrogen example:** Target 150 lb N per acre with urea. 150 ÷ 0.46 = **326 lb urea per acre**.

**Phosphate example:** Target 60 lb P2O5 per acre with DAP. 60 ÷ 0.46 = 130 lb DAP, and that DAP also supplies 130 × 0.18 = **23.5 lb of N**. Subtract that from your nitrogen need before calculating the urea.

## Start with a soil test
A soil test tells you whether P and K are likely to limit yield. Nitrogen recommendations usually come from yield goal, previous crop and soil type rather than a standard test. Your state extension service publishes rates that fit local soils and weather.

## Nitrogen losses
Nitrogen moves and changes form. Common loss paths include leaching in coarse soils, denitrification in saturated soils and ammonia volatilization from surface-applied urea. Using the 4R approach (right source, right rate, right time, right place) reduces losses and protects water quality.

## Do the math with real prices
Fertilizer is sold by the ton, but crops respond to pounds of nutrient. Compare cost per pound of nutrient across products, not price per ton. Use the [Fertilizer Calculator]({R}tools/fertilizer-calculator.html) to convert targets to product and estimate cost for your acres.
"""),
dict(slug="usda-plant-hardiness-zones-explained", cat="Climate & Soil", title="USDA Plant Hardiness Zones Explained (2023 Map)",
 desc="How USDA hardiness zones work, what changed in the 2023 map, and what the zones do and do not tell you about growing crops.",
 tools=["growing-degree-days-calculator"], related=["growing-degree-days-guide","soil-testing-and-ph-guide","crop-rotation-basics"],
 sources=[("USDA Plant Hardiness Zone Map","https://planthardiness.ars.usda.gov"),("USDA Agricultural Research Service","https://www.ars.usda.gov")],
 body="""
The USDA Plant Hardiness Zone Map is the standard guide for which perennial plants can survive winter cold in a given location. Gardeners, orchardists and nursery growers use it every day, and it appears on most seed and plant labels in the United States.

## How the zones work
The map divides the country into **13 zones**. Each zone represents a 10°F band of the average annual extreme minimum temperature, which is the coldest night of the year averaged over many years. Each zone is further split into "a" and "b" halves that are 5°F apart.

| Zone | Average annual extreme minimum |
|---|---|
| 3a | -40 to -35°F |
| 5a | -20 to -15°F |
| 6a | -10 to -5°F |
| 7a | 0 to 5°F |
| 8a | 10 to 15°F |
| 9a | 20 to 25°F |

## What changed in the 2023 update
USDA released an updated map in November 2023 using weather station data from 1991 to 2020. Compared with the 2012 map, many locations moved about half a zone warmer. A farm that was in zone 6a on the old map may now show 6b or 7a. The change reflects recent winter temperatures; it does not guarantee that a particular plant will now survive.

## What hardiness zones do not tell you
- **Heat and humidity.** A plant can survive winter cold in a zone but fail in hot summers.
- **Frost dates.** Last spring frost and first fall frost matter more for annual vegetables and row crops.
- **Rainfall, snow cover and wind.** Snow insulates roots; dry winter wind desiccates evergreens.
- **Soil drainage and microclimate.** A south-facing slope or a low frost pocket can be a full zone different.

## Which growers should care
Hardiness zones matter most for fruit trees, berries, grapes, asparagus, perennial forages and landscape plantings. For annual crops such as corn and soybeans, **frost dates and growing degree days** give a better planning picture. See our [growing degree days guide]({R}blog/growing-degree-days-guide.html).

## How to find your zone
Enter your ZIP code on the official USDA map site, then compare the result with your own experience of winter lows. If you grow near the edge of a zone, choose plants rated one zone colder than your site for extra margin.
"""),
dict(slug="usda-farm-programs-guide", cat="Programs", title="USDA Farm Programs Explained: Loans, Insurance and Conservation",
 desc="A plain-English overview of major USDA programs for U.S. farmers: FSA loans, crop insurance, ARC and PLC, EQIP, CSP and CRP, and where to apply.",
 tools=["crop-profit-calculator"], related=["crop-budget-break-even-guide","soil-testing-and-ph-guide","crop-rotation-basics"],
 sources=[("Farmers.gov","https://www.farmers.gov"),("USDA Farm Service Agency","https://www.fsa.usda.gov"),("USDA Risk Management Agency","https://www.rma.usda.gov"),("USDA NRCS","https://www.nrcs.usda.gov")],
 body="""
The U.S. Department of Agriculture runs several programs that help farmers finance operations, manage risk and conserve natural resources. This guide explains the major ones in plain English. Details change with each farm bill and annual funding, so always confirm current rules before you apply.

## Farm Service Agency (FSA) loans
FSA offers direct farm ownership and operating loans, and guarantees loans made by commercial lenders. Programs include **microloans** for smaller operations and funds aimed at **beginning, veteran and underserved farmers**. FSA is often a lender of last resort for applicants who cannot get credit elsewhere on reasonable terms, and requirements, interest rates and loan limits are updated regularly.

## Federal crop insurance
Crop insurance is administered by the Risk Management Agency (RMA) and sold through private insurance agents. Common coverage types include:
- **Yield Protection:** pays when yield falls below a guaranteed level.
- **Revenue Protection:** protects against a drop in yield, price or both.
- **Whole-Farm and specialty options** for diversified or specialty crops, where available.

Premiums are subsidized, and sales closing dates differ by crop and county, so talk to an agent well before planting.

## ARC and PLC commodity programs
Agriculture Risk Coverage (ARC) and Price Loss Coverage (PLC) are FSA programs that can make payments when prices or revenues fall below benchmarks for covered commodities. Producers generally enroll on a schedule set by FSA, and the choice between ARC and PLC depends on your crop mix and market outlook.

## Conservation programs
- **EQIP (NRCS):** cost-share for practices such as cover crops, nutrient management and irrigation efficiency.
- **CSP (NRCS):** payments for maintaining and improving conservation on working lands.
- **CRP (FSA):** annual rental payments for taking environmentally sensitive land out of production under contract.

## How to get started
1. Visit your local USDA Service Center. You can find it through farmers.gov.
2. Ask about establishing a **farm number** with FSA, which many programs require.
3. Gather records: yields, acreage, tax returns, and a basic budget.
4. Ask each agency for current deadlines, since many are seasonal.

> **Tip:** Run a budget before you borrow. Our [Crop Profit Calculator]({R}tools/crop-profit-calculator.html) shows your break-even price and yield so you can judge whether a loan or insurance level makes sense.
"""),
dict(slug="crop-rotation-basics", cat="Planning", title="Crop Rotation Basics: Why It Works and How to Plan It",
 desc="How crop rotation reduces pests, improves yield and manages nitrogen, with a simple three-year rotation example.",
 tools=["fertilizer-calculator","crop-profit-calculator"], related=["npk-fertilizer-labels-explained","seeding-rate-corn-soybeans","soil-testing-and-ph-guide"],
 sources=[("USDA NRCS Conservation Practices","https://www.nrcs.usda.gov"),("USDA Economic Research Service","https://www.ers.usda.gov")],
 body="""
Crop rotation means growing different crops in a planned sequence on the same field. It is one of the oldest and most reliable tools in farming, and it still earns its place because it affects yield, input costs and risk at the same time.

## Why rotation works
- **Breaks pest and disease cycles.** Many insects, nematodes and diseases build up when the same crop is grown year after year. Corn rootworm and soybean cyst nematode are two well-known examples.
- **Rotation yield benefit.** Corn after soybeans commonly yields more than corn after corn. The gap is often in the range of 5 to 15 percent, depending on weather, soil and management.
- **Nitrogen credit.** Legumes such as soybeans and alfalfa leave residue that releases nitrogen for the next crop. Credits vary by state and crop, so check your extension recommendations rather than assuming a number.
- **Weed management.** Different crops allow different herbicide modes of action and different planting and harvest dates, which slows herbicide resistance.
- **Soil protection.** Diverse root systems and cover crops improve structure and reduce erosion.

## A simple three-year example
| Year | Crop | Why it fits |
|---|---|---|
| 1 | Corn | Uses nitrogen, high residue |
| 2 | Soybeans | Adds N credit, breaks corn pests |
| 3 | Winter wheat + cover crop | Spreads workload, protects soil over winter |

Many Corn Belt farms run a simple two-year corn and soybean rotation. Adding a third crop typically improves the rotation effect and spreads risk, but it needs equipment, markets and storage that fit your area.

## Planning tips
1. Map each field's last three crops before ordering inputs.
2. Keep herbicide carryover restrictions in mind when choosing the next crop.
3. Budget each rotation, not each crop. A lower-margin year in the rotation may raise profit in the next.
4. Add cover crops where erosion or compaction is an issue.
5. Keep records so you can spot problem fields early.

## The money side
Rotation changes seed, fertilizer, chemical and machinery costs. Run each crop through a budget and compare returns across the whole sequence with our [Crop Profit Calculator]({R}tools/crop-profit-calculator.html). Use the [Fertilizer Calculator]({R}tools/fertilizer-calculator.html) to adjust nitrogen after a legume.
"""),
dict(slug="irrigation-water-calculations", cat="Water", title="Irrigation Water Calculations: Acre-Inches, Gallons and Pumping Time",
 desc="Learn the key irrigation formulas: acre-inches to gallons, system efficiency, and how long to pump to apply a target depth.",
 tools=["irrigation-water-calculator","land-area-converter"], related=["crop-budget-break-even-guide","soil-testing-and-ph-guide","growing-degree-days-guide"],
 sources=[("USDA NRCS Irrigation Guide","https://www.nrcs.usda.gov"),("USDA ERS Irrigation & Water Use","https://www.ers.usda.gov")],
 body="""
Irrigation math comes down to a few constants and one idea: you are putting a depth of water over an area. If you know the depth, the area and how efficient your system is, you can work out total volume and pumping time.

## Key conversions
- **1 acre-inch** = 1 inch of water over 1 acre = **27,154 gallons**
- **1 acre-foot** = 12 acre-inches = **325,851 gallons**
- **About 452 gallons per minute** pumped for one hour delivers roughly 1 acre-inch

## Account for efficiency
Not all the water you pump reaches the root zone. Losses come from evaporation, wind drift, runoff and deep percolation. Typical application efficiencies are roughly 75 to 90 percent for well-managed center pivots, higher for drip systems and often lower for surface (flood or furrow) irrigation. Use your own system's tested value when you have it.

> **Gross depth = Net depth needed ÷ Efficiency**

## Worked example
You want to apply a net 1.0 inch to 80 acres with an 85% efficient pivot.
1. Gross depth = 1.0 ÷ 0.85 = **1.18 inches**
2. Total water = 80 acres × 1.18 in = **94.1 acre-inches**
3. Gallons = 94.1 × 27,154 = about **2.56 million gallons**
4. At 800 GPM: 2,555,700 ÷ 800 = 3,195 minutes = **53.2 hours**

## How much to apply
Net depth depends on crop water use (evapotranspiration), rainfall and how much water your soil can store. Many state extension services publish crop water use charts and scheduling tools. Sandy soils hold less water and need lighter, more frequent applications; silt and clay loams hold more.

## Practical tips
- Measure actual pump output; wells decline and pressure changes affect flow.
- Check nozzle packages and pivot speed annually.
- Irrigate by soil moisture or ET rather than by the calendar.
- Know your state's water-right and reporting rules. In many western states these are strictly enforced.

Run your own numbers with the [Irrigation Water Calculator]({R}tools/irrigation-water-calculator.html).
"""),
dict(slug="grain-bushel-weights-and-bin-capacity", cat="Grain & Storage", title="Grain Bushel Weights and Bin Capacity: How to Calculate Both",
 desc="Standard test weights for corn, soybeans, wheat and more, plus the formula to estimate how many bushels a round grain bin holds.",
 tools=["grain-bushel-converter","grain-bin-capacity-calculator"], related=["crop-budget-break-even-guide","seeding-rate-corn-soybeans","irrigation-water-calculations"],
 sources=[("USDA Federal Grain Inspection Service","https://www.ams.usda.gov"),("USDA NASS","https://www.nass.usda.gov")],
 body="""
A bushel is a measure of volume, but markets convert it to weight using standard test weights. Knowing both lets you convert yields, check scale tickets and estimate bin capacity before harvest.

## Standard pounds per bushel
| Grain | Pounds per bushel |
|---|---|
| Corn (shelled) | 56 |
| Soybeans | 60 |
| Wheat | 60 |
| Barley | 48 |
| Oats | 32 |
| Sorghum (milo) | 56 |
| Rye | 56 |

Markets also use a **standard moisture level** when pricing, commonly 15% for corn, 13% for soybeans and about 13.5% for wheat. Grain that is wetter is discounted or dried; drier grain loses weight without losing bushels on paper.

## Convert weight to bushels
> **Bushels = Pounds ÷ Pounds per bushel**

A load of corn that nets 56,000 lb is 1,000 bushels. To go from bushels per acre to metric, multiply pounds per acre by 1.12085 to get kilograms per hectare. For example, 200 bu/ac of corn is 11,200 lb/ac, or about 12,554 kg/ha.

## Estimating round bin capacity
One bushel occupies about 1.2445 cubic feet, so a cubic foot holds about 0.8036 bushels.

> **Cylinder bushels = π × (diameter ÷ 2)² × grain depth × 0.8036**

**Example:** A 30-foot bin filled 24 feet deep. The base area is 706.9 sq ft. Volume = 706.9 × 24 = 16,965 cu ft. Bushels = 16,965 × 0.8036 = about **13,630 bu**.

For a peaked top, add a cone: base area × peak height ÷ 3 × 0.8036. A 5-foot peak on that bin adds about **950 bu**.

## Accuracy notes
- Deep grain packs under its own weight, so real capacity can be a few percent higher.
- Test weight, moisture and foreign material change how much fits.
- Bins with hoppers, tunnels or aeration floors need adjustments.
- Always confirm with the manufacturer's rated capacity before you plan a delivery.

Use the [Grain Bin Capacity Calculator]({R}tools/grain-bin-capacity-calculator.html) and [Grain Bushel Converter]({R}tools/grain-bushel-converter.html) to check your numbers.
"""),
dict(slug="soil-testing-and-ph-guide", cat="Climate & Soil", title="Soil Testing and pH: How to Sample, Read Results and Apply Lime",
 desc="How to take a representative soil sample, understand pH and nutrient results, and decide whether lime or fertilizer is needed.",
 tools=["fertilizer-calculator","land-area-converter"], related=["npk-fertilizer-labels-explained","crop-rotation-basics","usda-plant-hardiness-zones-explained"],
 sources=[("USDA NRCS Soil Health","https://www.nrcs.usda.gov"),("USDA Agricultural Research Service","https://www.ars.usda.gov")],
 body="""
A soil test is the cheapest way to decide where fertilizer and lime will pay off and where they will not. Good results depend on good sampling, so a few minutes of care in the field matter more than the lab you choose.

## How to take a representative sample
1. **Divide fields into management zones.** Different soil types, slopes, histories or crops should be sampled separately.
2. **Take many cores.** Combine roughly 15 to 20 cores from a zone into one composite sample. Zig-zag across the area and avoid fence rows, old manure piles and wet spots.
3. **Use a consistent depth.** Many labs recommend about 6 to 8 inches for tilled fields. Follow your lab's instructions, and take the same depth every time.
4. **Mix, dry and label.** Mix the cores in a clean plastic bucket, remove a sub-sample, and label it with field name and date.
5. **Sample on a schedule.** Every 2 to 4 years at the same time of year makes trends easy to see.

Use a lab that follows your state's recommended methods. Many labs take part in proficiency programs such as the North American Proficiency Testing Program.

## Understanding soil pH
pH measures acidity on a scale where 7 is neutral. It controls how available nutrients are and how well microbes and roots work.

| Crop type | Typical target pH |
|---|---|
| Corn, soybeans, small grains | 6.0 to 7.0 |
| Alfalfa | 6.5 to 7.0 |
| Blueberries | 4.5 to 5.5 |

Targets vary by crop and state, so check your extension guidelines.

## Lime and fertilizer
When pH is below target, agricultural lime (mostly calcium carbonate or dolomite) raises it. Lime need depends on the **buffer pH or lime requirement test**, not on pH alone, because soils with more clay and organic matter resist change. Lime products are rated by **calcium carbonate equivalent** and particle size, so compare products on effective neutralizing value.

Nutrient results are reported in parts per million (ppm) with ratings such as low, optimum or high. Your lab or extension service converts those ratings to pounds per acre of P2O5 and K2O, which you can plan with the [Fertilizer Calculator]({R}tools/fertilizer-calculator.html).

## Beyond pH, P and K
Organic matter, cation exchange capacity (CEC) and micronutrients such as zinc and sulfur can matter on certain soils and crops. Add them to your test when you suspect a problem.
"""),
dict(slug="sprayer-calibration-guide", cat="Equipment", title="Sprayer Calibration Guide: GPA Formula, Catch Test and Tank Mixes",
 desc="Calibrate a boom sprayer step by step: gallons per acre formula, travel speed check, nozzle catch test and tank mix math.",
 tools=["sprayer-calibration-calculator"], related=["crop-budget-break-even-guide","growing-degree-days-guide","grain-bushel-weights-and-bin-capacity"],
 sources=[("USDA NRCS Pest Management","https://www.nrcs.usda.gov"),("USDA Agricultural Research Service","https://www.ars.usda.gov")],
 body="""
A sprayer that is off by 10 percent wastes chemical or leaves weeds and pests uncontrolled. Calibration confirms how many gallons per acre (GPA) you are really applying, and it takes less than an hour.

## The GPA formula
> **GPA = (GPM per nozzle × 5,940) ÷ (Speed in mph × Nozzle spacing in inches)**

**Example:** Nozzles flow 0.40 GPM, you drive 10 mph, and nozzles are spaced 20 inches apart.
GPA = (0.40 × 5,940) ÷ (10 × 20) = 2,376 ÷ 200 = **11.88 GPA**.

## Step-by-step calibration
1. **Inspect and clean.** Replace worn, damaged or mismatched nozzles. Check screens and hoses.
2. **Measure nozzle spacing** in inches.
3. **Check travel speed.** Mark a known distance, such as 200 feet, in the field. Drive it at your spray speed and time it. Speed in mph = feet ÷ seconds × 0.682. For 200 ft in 15 seconds, that is about 9.1 mph.
4. **Run a catch test.** With clean water, collect output from each nozzle for one minute at working pressure. Convert ounces to gallons (128 oz per gallon). Replace nozzles that differ by more than about 5 percent from the average.
5. **Calculate GPA** and adjust speed, pressure or nozzle size until it matches the label.

## Pressure and flow
Nozzle flow changes with the square root of pressure, so to double flow you need about four times the pressure. Use nozzle size to make big changes and pressure for small ones, and stay within the nozzle's rated pressure to keep droplet size and drift under control.

## Tank mix math
> **Acres per tank = Tank size ÷ GPA**
> **Product per tank = Label rate per acre × Acres per tank**

With a 500-gallon tank at 11.88 GPA, one tank covers 42.1 acres. A product at 32 oz per acre needs about 1,347 oz per tank.

## Safety and compliance
The label is the law. Follow rates, water volumes, nozzle types, buffer zones, weather limits and protective equipment requirements exactly. Triple-rinse containers and keep application records.

Use the [Sprayer Calibration Calculator]({R}tools/sprayer-calibration-calculator.html) to do the math quickly in the field.
"""),
dict(slug="growing-degree-days-guide", cat="Climate & Soil", title="Growing Degree Days (GDD): What They Are and How to Use Them",
 desc="Understand growing degree days, the corn 86/50 method, and how GDD helps plan planting, hybrid maturity and harvest.",
 tools=["growing-degree-days-calculator"], related=["usda-plant-hardiness-zones-explained","seeding-rate-corn-soybeans","irrigation-water-calculations"],
 sources=[("USDA Agricultural Research Service","https://www.ars.usda.gov"),("USDA NASS Crop Progress","https://www.nass.usda.gov")],
 body="""
Calendar days are a poor measure of crop development because a cool week and a hot week are not equal. **Growing degree days (GDD)**, also called heat units, count how much useful warmth a crop receives, so you can predict stages such as emergence, silking and maturity.

## The GDD formula
> **GDD = (Daily high + Daily low) ÷ 2 − Base temperature**

For corn, sorghum and soybeans the common approach is the **86/50 method**:
- If the high is above 86°F, use 86.
- If the low is below 50°F, use 50.
- Base temperature is 50°F.
- GDD is never negative.

**Example 1:** High 90°F, low 60°F. Cap the high at 86. GDD = (86 + 60) ÷ 2 − 50 = **23**.

**Example 2:** High 72°F, low 45°F. Raise the low to 50. GDD = (72 + 50) ÷ 2 − 50 = **11**.

Add daily values from planting to get the season's accumulated GDD. Small grains often use a lower base temperature, so use the base recommended by your extension service.

## Typical corn milestones
- **Emergence:** roughly 100 to 120 GDD after planting.
- **Black layer (physiological maturity):** commonly 2,400 to 2,800 GDD for most hybrids, depending on relative maturity.

Seed companies list GDD ratings for hybrids, which lets you match maturity to your growing season length.

## How growers use GDD
- **Hybrid selection:** choose a hybrid that reaches black layer well before your average first fall frost.
- **Planting decisions:** compare how many GDD remain if planting is delayed.
- **Scouting and timing:** pests such as corn borer and weeds are often predicted by accumulated GDD.
- **Harvest planning:** estimate when grain will dry down.

## Where to find GDD data
State climate offices and land-grant universities provide GDD maps and calculators based on weather station data. You can also keep your own record from a local thermometer using the [Growing Degree Days Calculator]({R}tools/growing-degree-days-calculator.html).
"""),
dict(slug="crop-budget-break-even-guide", cat="Planning", title="Crop Budgets and Break-Even Prices: A Practical Guide",
 desc="How to build a simple crop budget, calculate break-even price and yield, and use the numbers to make better marketing and input decisions.",
 tools=["crop-profit-calculator","seed-rate-calculator","fertilizer-calculator"], related=["usda-farm-programs-guide","crop-rotation-basics","irrigation-water-calculations"],
 sources=[("USDA ERS Commodity Costs and Returns","https://www.ers.usda.gov"),("USDA NASS","https://www.nass.usda.gov")],
 body="""
Every acre has a price at which it stops losing money. Knowing that number before you plant gives you a clear benchmark for marketing, input spending and rented-land decisions.

## The basic budget
For each crop and field, list expected revenue and every cost per acre:

- **Revenue:** expected yield × expected price.
- **Variable costs:** seed, fertilizer, crop protection, insurance, fuel and repairs, hired labor, drying and hauling, interest on operating loans.
- **Fixed costs:** land rent or ownership cost, machinery depreciation, overhead.

> **Net return per acre = Revenue per acre − Total cost per acre**

## Break-even formulas
> **Break-even price = Total cost per acre ÷ Expected yield**
> **Break-even yield = Total cost per acre ÷ Expected price**

**Illustration (numbers are examples only):** Expected yield 200 bu/ac, price $4.50/bu, total cost $780/ac.
- Revenue = 200 × 4.50 = **$900/ac**
- Net return = 900 − 780 = **$120/ac**
- Break-even price = 780 ÷ 200 = **$3.90/bu**
- Break-even yield = 780 ÷ 4.50 = **173 bu/ac**

## Using break-even numbers
- **Marketing:** set price targets above your break-even, not just above last year's price.
- **Rented ground:** compare what you can afford to pay in rent against your expected net before costs.
- **Input decisions:** ask whether an extra input is likely to add enough bushels to pay for itself at your expected price.
- **Stress test:** recalculate with yield down 10% and price down 10% to see how much cushion you have.

## Good sources for cost data
The USDA Economic Research Service publishes national and regional cost-and-return estimates by commodity, and many land-grant universities publish enterprise budgets for your state. Use them as checks, then replace averages with your own records.

## Common budgeting mistakes
1. Using the best field's yield for every field.
2. Leaving out family labor, machinery ownership or interest.
3. Ignoring drying, hauling and storage costs.
4. Forgetting that insurance and program payments are separate from market revenue.

Run the numbers with the [Crop Profit Calculator]({R}tools/crop-profit-calculator.html).
"""),
]
