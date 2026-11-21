import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "storage" / "uploads"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

def create_pdf(filename: str, title: str, author: str, pages_content: list):
    filepath = SAMPLE_DIR / filename
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    story = []

    for page_idx, page_sections in enumerate(pages_content):
        if page_idx == 0:
            story.append(Paragraph(title, title_style))
            story.append(Paragraph(author, meta_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=12))

        for heading, paragraph in page_sections:
            story.append(Paragraph(heading, h1_style))
            story.append(Paragraph(paragraph, body_style))

        if page_idx < len(pages_content) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"Generated sample document: {filepath}")
    return filepath

def generate_all_samples():
    # Document 1: Dr. Elena Vance (2024)
    create_pdf(
        filename="Solid_State_Batteries_Vance_2024.pdf",
        title="Solid-State vs. Lithium-Ion Batteries: Thermal Stability and Fast-Charging Dynamics",
        author="Dr. Elena Vance, Senior Fellow in Energy Materials, Institute of Advanced Storage (2024)",
        pages_content=[
            # Page 1
            [
                ("1. Abstract & Electrochemical Architecture",
                 "Solid-state battery architectures utilizing garnet-type ceramic electrolytes (LLZO) offer a transformative leap over conventional liquid organic electrolyte lithium-ion cells. Our experimental trials demonstrate complete suppression of dendritic short circuits under continuous cycling, enabling unprecedented volumetric energy densities of 450 Wh/kg."),
                ("2. Safety and Thermal Runaway Prevention",
                 "Unlike volatile alkyl carbonate solvents that experience explosive thermal runaway at 130°C, the ceramic-composite separator remains inert up to 280°C. In nail-penetration and overcharge experiments, zero combustion or hazardous venting was recorded across 50 tested prismatic cells.")
            ],
            # Page 2
            [
                ("3. Fast-Charging Cycle Durability Under 4C Rates",
                 "A primary bottleneck in earlier solid-state literature was interfacial resistance under rapid charge cycles. Here, by applying a nanometer-thin lithium-tin alloy buffer layer, our experimental cells maintained 84.5% capacity retention after 2,000 continuous charge-discharge cycles at an extreme 4C charging rate. We recommend pre-heating the battery pack to 45°C prior to ultrafast charging, as elevated thermal kinetics dramatically reduce interfacial impedance and eliminate void nucleation."),
                ("4. Low-Temperature Conductivity Metrics",
                 "At sub-zero temperatures (-20°C), bulk ionic conductivity remained above 1.2 mS/cm. The pack achieved 76% usable capacity without external auxiliary heating, outperforming conventional NCA liquid chemistry by 28%.")
            ],
            # Page 3
            [
                ("5. Manufacturing Scalability and Cost Parity",
                 "Using continuous roll-to-roll dry-coating equipment, our pilot line demonstrated a defect-free continuous film production rate of 15 meters per minute. We model cell production costs dropping to $72 per kWh by 2027 at a 20 GWh manufacturing scale, achieving direct parity with traditional lithium iron phosphate (LFP)."),
                ("6. Concluding Remarks",
                 "Solid-state systems are technically ready for high-performance automotive platforms, delivering 2,000-cycle longevity at 4C rates when controlled at 45°C.")
            ]
        ]
    )

    # Document 2: Prof. Marcus Chen (2023)
    create_pdf(
        filename="Automotive_Cell_Degradation_Chen_2023.pdf",
        title="Commercialization Pathways and Life-Cycle Degradation in Next-Gen Automotive Battery Cells",
        author="Prof. Marcus Chen, Automotive Engineering Laboratory, Tokyo Institute of Technology (2023)",
        pages_content=[
            # Page 1
            [
                ("1. Executive Summary & Problem Scope",
                 "While solid-state and silicon-anode cells demonstrate high initial energy density in coin-cell laboratory conditions, large-format automotive pouch cells encounter catastrophic mechanical shear and interfacial contact loss during realistic driving profiles."),
                ("2. Mechanical Shear and Interfacial Impedance",
                 "Volumetric breathing during lithiation causes microscopic delamination at the solid electrolyte-electrode interface. In our accelerated stress testing, contact loss resulted in localized current constriction, causing premature capacity fade.")
            ],
            # Page 2
            [
                ("3. High C-Rate Degradation and Contradictory Cycling Limits",
                 "In direct contradiction to optimistic laboratory reports, our rigorous automotive stress testing shows that solid-state cell capacity retention drops precipitously to 63.8% after only 850 cycles when subjected to repeated 4C charging. Furthermore, our findings strongly warn against operating temperatures above 40°C. Operating at 45°C triggers rapid electrolyte decomposition, accelerates interphase impedance by 340%, and induces microscopic lithium filament short circuits."),
                ("4. Optimal Thermal Management Protocols",
                 "We conclude that automotive battery management systems (BMS) must strictly clamp fast-charging temperatures between 25°C and 35°C to preserve long-term cycle life and prevent void formation.")
            ],
            # Page 3
            [
                ("5. Economic Reality and Commercialization Hurdles",
                 "Our techno-economic assessment indicates that cleanroom and dry-room humidity requirements (dew point < -50°C) severely restrict factory throughput. Pilot line yields currently hover below 48%. We project that commercial solid-state cell costs will remain above $115 per kWh until at least 2030, rendering broad market passenger EV adoption economically unviable in the near term."),
                ("6. Strategic Assessment",
                 "Liquid electrolyte chemistries with advanced silicon-carbon composite anodes remain the only viable cost-effective solution for passenger electric vehicles through 2030.")
            ]
        ]
    )

    # Document 3: Dr. Sarah Jenkins (2024)
    create_pdf(
        filename="Grid_EV_Integration_Jenkins_2024.pdf",
        title="Grid-Scale EV Integration: Charging Infrastructure, Degradation Tradeoffs, and Economic Feasibility",
        author="Dr. Sarah Jenkins, Clean Transportation Grid Institute, UC Berkeley (2024)",
        pages_content=[
            # Page 1
            [
                ("1. Abstract & Urban Distribution Impact",
                 "Uncontrolled simultaneous adoption of 350 kW DC fast chargers presents an existential risk to municipal distribution transformers. We analyzed 1,200 grid nodes across California and observed feeder voltage sags exceeding 8.4% during peak 5:00 PM to 8:00 PM charging spikes."),
                ("2. Transformer Life Expectancy Reduction",
                 "High coincident peak demand raises transformer winding temperatures to 125°C, reducing transformer operational life from 30 years to under 7.5 years in suburban substations without managed charging controls.")
            ],
            # Page 2
            [
                ("3. Fast Charging vs. Battery Degradation Tradeoffs",
                 "Consistent with automotive degradation literature, our grid study finds that fleet vehicles utilizing daily fast charging (>1.5C) experience 2.2x faster capacity degradation compared to vehicles using Level 2 overnight charging (0.2C). To balance grid stability with vehicle longevity, we propose dynamic pricing incentives where charging rates above 2C are tariffed at 3x the baseline wholesale electricity rate."),
                ("4. Vehicle-to-Grid (V2G) Bi-Directional Power",
                 "Fleet V2G participation can supply 14 MW of flexible peak capacity per 10,000 participating passenger vehicles, yielding fleet owners an estimated annual revenue of $620 per vehicle while dampening grid frequency variations.")
            ],
            # Page 3
            [
                ("5. Stationary Battery Storage Buffer Economics",
                 "Installing stationary 1 MWh battery energy storage system (BESS) buffer units at DC fast charging plazas eliminates utility grid upgrade connection fees of up to $1.2 million per station. Peak shaving lowers demand charges by 58%."),
                ("6. Policy Recommendations",
                 "Municipalities should mandate smart load management and prioritize 8-hour overnight smart charging rather than rapid multi-megawatt charging depots for suburban passenger commutes.")
            ]
        ]
    )

if __name__ == "__main__":
    generate_all_samples()
