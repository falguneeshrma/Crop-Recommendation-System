import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "knowledge_base")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(HERE, "crop_stats.json")) as f:
    STATS = json.load(f)

AGRONOMY = {
"rice": {
    "overview": "A staple cereal grown widely in flooded (paddy) or upland systems across South and Southeast Asia. Needs standing water for most of its growth cycle in the paddy method.",
    "soil": "Prefers clayey or loamy soil with good water retention. Puddled fields are standard for transplanted rice.",
    "fertilizer": "Apply nitrogen in split doses (basal + tillering + panicle initiation) to avoid lodging and maximize grain fill. Phosphorus is best applied fully at basal stage; potassium split between basal and panicle stage.",
    "irrigation": "Requires continuous flooding (2-5 cm standing water) through most stages, with alternate wetting-drying possible to save water without major yield loss.",
    "pests": "Common threats: stem borer, brown planthopper, leaf folder, and blast disease (fungal). Rotate varieties and avoid excess nitrogen to reduce blast risk.",
    "harvest": "Typically ready 100-150 days after transplanting, depending on variety. Harvest when 80-85% of grains have turned golden yellow.",
},
"maize": {
    "overview": "A versatile cereal (corn) grown as food, feed, and industrial raw material. Grows well in a wide range of climates.",
    "soil": "Well-drained loamy soil with good organic matter. Sensitive to waterlogging.",
    "fertilizer": "Heavy nitrogen feeder; split nitrogen application at sowing, knee-high stage, and tasseling gives best results. Phosphorus supports root and early growth; potassium improves stalk strength and disease resistance.",
    "irrigation": "Critical irrigation windows are at knee-high stage, tasseling/silking, and grain filling — moisture stress during silking sharply cuts yield.",
    "pests": "Fall armyworm is the major modern threat; also stem borer and maize streak virus. Scout weekly during vegetative stage.",
    "harvest": "Grain maize matures in 90-120 days; harvest when husks dry and kernels reach physiological maturity (black layer at kernel base).",
},
"chickpea": {
    "overview": "A cool-season pulse (gram) valued for protein content, grown mainly as a rabi (winter) crop in semi-arid regions.",
    "soil": "Well-drained sandy loam to clay loam with neutral to slightly alkaline pH. Poor tolerance for waterlogging.",
    "fertilizer": "Being a legume, it fixes atmospheric nitrogen via root nodules — needs only a small starter dose of nitrogen, with phosphorus being the key nutrient to support nodulation.",
    "irrigation": "Mostly grown as a rainfed crop; if irrigated, critical stages are branching and pod filling. Avoid irrigation at flowering to reduce flower drop.",
    "pests": "Pod borer (Helicoverpa) is the major pest; wilt (Fusarium) is the key disease — use resistant varieties and seed treatment.",
    "harvest": "Matures in 90-120 days. Harvest when plants turn yellowish-brown and pods rattle when shaken.",
},
"kidneybeans": {
    "overview": "A legume grown for its large colorful seeds (rajma), popular in cooler climates and higher elevations.",
    "soil": "Well-drained loamy soil with good organic matter; sensitive to both drought and waterlogging.",
    "fertilizer": "Light nitrogen starter dose since it's a nitrogen-fixing legume; phosphorus and potassium support pod development and seed size.",
    "irrigation": "Needs consistent moisture, especially at flowering and pod-filling; avoid water stress during these windows.",
    "pests": "Bean beetle, aphids, and anthracnose/bacterial blight are common issues. Use certified disease-free seed.",
    "harvest": "Ready in 90-120 days. Harvest dry beans when pods rattle and have fully dried on the plant.",
},
"pigeonpeas": {
    "overview": "A drought-tolerant perennial legume (tur/arhar) widely grown in semi-arid tropics, often intercropped with cereals.",
    "soil": "Adapts to a wide range of soils but performs best in well-drained loamy soil; intolerant of waterlogging.",
    "fertilizer": "Minimal nitrogen needed due to nitrogen fixation; phosphorus at sowing boosts nodulation and early growth.",
    "irrigation": "Highly drought tolerant with a deep root system; mostly rainfed, with irrigation only critical at flowering/pod-filling in dry spells.",
    "pests": "Pod borer complex (Helicoverpa, Maruca) and wilt disease are major concerns; sterility mosaic virus is also significant.",
    "harvest": "Long duration crop (150-270 days depending on variety). Harvest when pods dry and turn brown.",
},
"mothbeans": {
    "overview": "An extremely drought-hardy legume traditionally grown in arid and semi-arid regions with minimal inputs.",
    "soil": "Thrives in sandy and light-textured soils with poor fertility; tolerates drought better than almost any other pulse.",
    "fertilizer": "Very low fertilizer requirement; a light phosphorus dose at sowing is usually enough given its nitrogen-fixing ability.",
    "irrigation": "Almost entirely rainfed; excels in low-rainfall regions where other legumes fail.",
    "pests": "Generally pest-hardy; yellow mosaic virus and pod borer can occur in wetter years.",
    "harvest": "Short duration crop (60-90 days), making it useful for double-cropping in arid zones.",
},
"mungbean": {
    "overview": "A fast-growing, short-duration legume (green gram) widely used as both a grain crop and a green manure.",
    "soil": "Well-drained sandy loam to loam soil; sensitive to waterlogging.",
    "fertilizer": "Minimal nitrogen needed due to nodulation; phosphorus and a small potassium dose improve pod set.",
    "irrigation": "Light, frequent irrigation is better than heavy flooding; critical at flowering and pod development.",
    "pests": "Yellow mosaic virus (spread by whitefly) is the major threat; also aphids and pod borer.",
    "harvest": "Very short duration (60-75 days), allowing it to fit well between two main crops in a rotation.",
},
"blackgram": {
    "overview": "A pulse crop (urad) grown in both kharif and rabi seasons, important for both food and soil-fertility benefits.",
    "soil": "Performs well on clay loam to loamy soils with good drainage; moderately tolerant of a range of pH.",
    "fertilizer": "Light starter nitrogen with a higher phosphorus dose to support nodulation and pod formation.",
    "irrigation": "Sensitive to both drought and excess moisture; critical irrigation at flowering and pod-filling stages.",
    "pests": "Yellow mosaic virus and powdery mildew are common; pod borer also affects yield.",
    "harvest": "Matures in 70-90 days; harvest when pods turn black and dry.",
},
"lentil": {
    "overview": "A cool-season pulse (masoor) grown mainly as a rabi crop, valued for high protein content and soil-enriching nitrogen fixation.",
    "soil": "Well-drained loamy soil with neutral pH; poor tolerance to waterlogging and salinity.",
    "fertilizer": "Low nitrogen requirement; phosphorus is the key input for nodulation and root development.",
    "irrigation": "Mostly rainfed; if irrigating, avoid excess water which encourages fungal disease and reduces nodulation.",
    "pests": "Aphids, pod borer, and rust/wilt diseases are the main concerns; seed treatment reduces soil-borne disease risk.",
    "harvest": "Matures in 100-130 days. Harvest when lower pods turn brown and leaves start shedding.",
},
"pomegranate": {
    "overview": "A hardy, drought-tolerant fruit shrub/small tree suited to semi-arid and Mediterranean-type climates.",
    "soil": "Adapts to a wide range of soils, including saline and alkaline, but performs best in well-drained loamy soil.",
    "fertilizer": "Balanced NPK with higher potassium during fruit development improves fruit size, color, and juice content. Apply farmyard manure annually.",
    "irrigation": "Drip irrigation is ideal — drought tolerant once established, but consistent moisture during fruit set and development improves fruit quality and reduces cracking.",
    "pests": "Fruit borer and bacterial blight are major concerns; fruit cracking is a physiological issue linked to irrigation inconsistency.",
    "harvest": "Fruit matures 5-7 months after flowering; harvest when the rind turns from green to pink/red and produces a metallic sound when tapped.",
},
"banana": {
    "overview": "A fast-growing tropical fruit crop grown year-round in warm, humid climates; propagated via suckers/tissue culture, not seed.",
    "soil": "Deep, well-drained, fertile loamy soil rich in organic matter; sensitive to waterlogging.",
    "fertilizer": "Very high nutrient demand — heavy potassium requirement in particular for bunch development, alongside substantial nitrogen; usually fertigated in split doses monthly.",
    "irrigation": "High water requirement year-round; drip irrigation with regular scheduling is standard in commercial cultivation.",
    "pests": "Panama wilt (Fusarium), Sigatoka leaf spot, and banana weevil are major concerns; use disease-free planting material.",
    "harvest": "Fruit matures 10-14 months after planting, roughly 3-4 months after flowering (bunch emergence). Harvest when fingers fill out and turn from angular to rounded.",
},
"mango": {
    "overview": "A long-lived tropical/subtropical fruit tree, often called the 'king of fruits', requiring several years to reach full bearing.",
    "soil": "Deep, well-drained loamy soil; tolerates a range of soil types but not waterlogging.",
    "fertilizer": "Moderate, age-graded NPK doses increasing as the tree matures; potassium is important for fruit quality and size, applied post-harvest and pre-flowering.",
    "irrigation": "Needs a distinct dry period before flowering to induce blossoming; irrigation resumes after fruit set and during fruit development, then tapers before harvest to improve sweetness.",
    "pests": "Mango hopper, fruit fly, and powdery mildew (on flowers) are the major threats.",
    "harvest": "Fruit matures 3-5 months after flowering. Harvest at physiological maturity (change in fruit shoulder shape and skin color) rather than full ripeness for better transport.",
},
"grapes": {
    "overview": "A perennial woody vine grown for table fruit, raisins, or wine, requiring trellising and a distinct pruning cycle.",
    "soil": "Well-drained sandy loam; grapevines are sensitive to waterlogged roots.",
    "fertilizer": "Balanced NPK with an emphasis on potassium during berry development to improve sugar content and color; timing is tied to the pruning/fruiting cycle.",
    "irrigation": "Requires controlled deficit irrigation — moderate water during vegetative growth, reduced water near veraison (color change) to concentrate sugars.",
    "pests": "Downy mildew, powdery mildew, and thrips are major concerns, especially in humid conditions.",
    "harvest": "From pruning to harvest is typically 100-140 days depending on variety and region. Harvest based on sugar content (Brix) rather than color alone.",
},
"watermelon": {
    "overview": "A warm-season vining fruit crop that spreads extensively and needs plenty of space and heat.",
    "soil": "Well-drained sandy loam warms quickly and suits its heat-loving nature; sensitive to waterlogging.",
    "fertilizer": "Moderate nitrogen early for vine growth, shifting to higher potassium during fruit development for sweetness; avoid excess nitrogen late, which delays fruiting.",
    "irrigation": "Needs consistent moisture through vine growth and fruit set, but reduced watering near harvest improves sugar concentration.",
    "pests": "Fruit fly, aphids (which spread viruses), and powdery mildew are common issues.",
    "harvest": "Matures 80-100 days after sowing. Harvest indicators: dried tendril nearest the fruit, dull skin sheen, and a hollow sound when tapped.",
},
"muskmelon": {
    "overview": "A warm-season vining fruit (cantaloupe) similar in cultivation needs to watermelon but generally shorter duration.",
    "soil": "Sandy loam with good drainage and warmth; poor tolerance for waterlogged conditions.",
    "fertilizer": "Balanced NPK during vegetative growth, with increased potassium during fruit maturation for sweetness.",
    "irrigation": "Regular irrigation through vine growth and fruit set; reduce watering as fruit nears maturity to concentrate sugars and avoid fruit splitting.",
    "pests": "Fruit fly and powdery mildew are the primary concerns; downy mildew in humid conditions.",
    "harvest": "Matures in 70-90 days. Harvest at 'full slip' stage — the fruit separates easily from the vine with a light twist.",
},
"apple": {
    "overview": "A temperate-climate deciduous fruit tree requiring winter chilling hours to break dormancy and flower properly.",
    "soil": "Well-drained loamy soil with slightly acidic to neutral pH; poor tolerance for waterlogging.",
    "fertilizer": "Balanced NPK, applied in early spring before bud break, with potassium supporting fruit size and quality; avoid late-season nitrogen which delays dormancy.",
    "irrigation": "Regular irrigation during fruit development is important, especially in the weeks before harvest for fruit sizing, tapering as maturity approaches.",
    "pests": "Codling moth, apple scab, and fire blight are major concerns in humid growing regions.",
    "harvest": "Matures 4-6 months after flowering depending on variety; harvest timing is based on background skin color change and starch-iodine testing.",
},
"orange": {
    "overview": "An evergreen citrus tree suited to subtropical climates, sensitive to frost but requiring some cool nights for good fruit color and sugar development.",
    "soil": "Well-drained sandy loam with slightly acidic pH; very sensitive to waterlogging (root rot risk).",
    "fertilizer": "Balanced NPK in split doses through the growing season, with micronutrients (zinc, iron) often needed on alkaline soils.",
    "irrigation": "Regular but not excessive irrigation; a brief mild moisture stress before flowering can improve bloom synchronization.",
    "pests": "Citrus canker, leaf miner, and fruit fly are common; huanglongbing (citrus greening), spread by psyllids, is a serious modern threat.",
    "harvest": "Fruit matures 7-12 months after flowering depending on variety. Harvest based on rind color change and sugar-acid ratio, since fruit doesn't ripen further after picking.",
},
"papaya": {
    "overview": "A fast-growing, short-lived tropical fruit tree that begins bearing within a year of planting, making it popular for quick returns.",
    "soil": "Well-drained sandy loam rich in organic matter; extremely sensitive to waterlogging, which quickly causes root rot.",
    "fertilizer": "High nutrient demand due to fast growth and continuous fruiting; regular split doses of NPK, with potassium supporting fruit quality.",
    "irrigation": "Consistent moisture needed year-round given continuous flowering/fruiting, but with excellent drainage to avoid root rot.",
    "pests": "Papaya ringspot virus (aphid-transmitted) is the most serious threat; also fruit fly and powdery mildew.",
    "harvest": "First harvest around 9-11 months after planting, then continuous harvesting. Pick when a slight color break appears at the fruit's blossom end.",
},
"coconut": {
    "overview": "A long-lived tropical palm central to coastal agriculture, valued for copra, oil, fiber, and water.",
    "soil": "Tolerant of a wide range of soils including sandy coastal soils; requires good drainage but consistent subsoil moisture.",
    "fertilizer": "Regular annual application of balanced NPK plus organic manure; potassium and chlorine (common salt) needs are notably higher than most crops due to the palm's physiology.",
    "irrigation": "Deep-rooted and moderately drought tolerant once mature, but consistent irrigation significantly improves nut yield, especially in dry seasons.",
    "pests": "Rhinoceros beetle and red palm weevil are major pests; bud rot disease can be fatal if untreated.",
    "harvest": "Begins bearing in 5-7 years; nuts mature roughly 12 months after pollination and are harvested year-round in cycles of 45-60 days.",
},
"cotton": {
    "overview": "A major fiber crop grown in warm climates with a long frost-free growing season, harvested for both lint and cottonseed.",
    "soil": "Deep, well-drained black cotton soil (vertisol) or loamy soil with good moisture-holding capacity.",
    "fertilizer": "Nitrogen is critical and applied in split doses through vegetative and boll-development stages; potassium is important for boll development and fiber quality.",
    "irrigation": "Sensitive to both drought and waterlogging; critical irrigation windows are flowering and boll development, with reduced water needed near maturity/boll opening.",
    "pests": "Bollworm complex (including pink bollworm) and whitefly (which spreads leaf curl virus) are the major threats; Bt cotton varieties target bollworm resistance.",
    "harvest": "Matures in 150-180 days; harvested in multiple pickings as bolls open over several weeks rather than all at once.",
},
"jute": {
    "overview": "A fast-growing fiber crop grown mainly in warm, humid, high-rainfall river-delta regions, used to produce natural fiber (burlap/hessian).",
    "soil": "Fertile, well-drained alluvial loamy soil with good water-holding capacity.",
    "fertilizer": "Moderate nitrogen for vegetative growth (fiber comes from stem tissue), with phosphorus and potassium supporting overall plant vigor.",
    "irrigation": "High rainfall requirement; often grown as a rainfed monsoon crop, with supplemental irrigation needed if rains are delayed.",
    "pests": "Stem weevil, semi-looper caterpillar, and stem rot are common issues in waterlogged conditions.",
    "harvest": "Harvested 100-120 days after sowing at the flowering stage, when fiber quality is optimal; stems are then retted in water to separate fiber.",
},
"coffee": {
    "overview": "A perennial shrub/small tree grown in tropical highlands, typically under partial shade, taking 3-4 years to reach first bearing.",
    "soil": "Deep, well-drained, slightly acidic loamy soil rich in organic matter.",
    "fertilizer": "Balanced NPK applied in split doses aligned with the flowering-fruiting cycle; potassium is particularly important for bean filling and quality.",
    "irrigation": "Needs a brief dry spell before flowering to trigger uniform blossoming ('blossom showers'), then consistent moisture through berry development.",
    "pests": "Coffee berry borer and leaf rust (a fungal disease) are the most damaging; shade management helps reduce leaf rust pressure.",
    "harvest": "Cherries ripen 7-9 months after flowering; harvested selectively as cherries turn red (for arabica) since ripening is uneven on the same branch.",
},
}


def format_range(vals):
    lo, hi, mean = vals
    return f"{lo}-{hi} (avg {mean})"


def build_doc(crop: str) -> str:
    s = STATS[crop]
    a = AGRONOMY[crop]
    name = crop.capitalize()
    doc = f"""# {name}

## Overview
{a['overview']}

## Ideal Growing Conditions (from historical field data, {os.environ.get('N_SAMPLES', '100')} samples)
- Nitrogen (N) in soil: {format_range(s['N'])} kg/ha
- Phosphorus (P) in soil: {format_range(s['P'])} kg/ha
- Potassium (K) in soil: {format_range(s['K'])} kg/ha
- Temperature: {format_range(s['temperature'])} °C
- Humidity: {format_range(s['humidity'])} %
- Soil pH: {format_range(s['ph'])}
- Rainfall: {format_range(s['rainfall'])} mm

## Soil Preference
{a['soil']}

## Fertilizer & Nutrient Management
{a['fertilizer']}

## Irrigation
{a['irrigation']}

## Common Pests & Diseases
{a['pests']}

## Harvesting
{a['harvest']}
"""
    return doc


def main():
    for crop in STATS:
        if crop not in AGRONOMY:
            print(f"WARNING: no agronomy entry for {crop}, skipping")
            continue
        doc = build_doc(crop)
        path = os.path.join(OUT_DIR, f"{crop}.md")
        with open(path, "w") as f:
            f.write(doc)
    print(f"Wrote {len(AGRONOMY)} knowledge base documents to {OUT_DIR}")


if __name__ == "__main__":
    main()
