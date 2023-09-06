from pandas import read_csv

from qee import Analysis
from qee.enums import VoltageValue
from qee.utils.center_print import center_print
from qee.utils.harmonics_cols import harmonics_cols

data = read_csv("data/csv/data.csv", sep=";")

TIME_LABEL = "Time"
vf_labels = ["V1_Avg [V]", "V2_Avg [V]", "V3_Avg [V]"]
# vf_labels = ["V1_Min [V]", "V2_Min [V]", "V3_Min [V]"]
vl_labels = ["V12_Avg [V]", "V23_Avg [V]", "V31_Avg [V]"]
# vl_labels = ["V12_Min [V]", "V23_Min [V]", "V31_Min [V]"]
voltage_labels = ["V1", "V2", "V3"]

analysis = Analysis(data)

print(center_print("Análise de Indicadores de QEE"))

print("\nVariação de tensão".center(50))
print("-" * 50)

for vf_label in vf_labels:
    print(f"\nIndicadores de variação de tensão para {vf_label}")
    # graphic = analysis.graphic_voltage(TIME_LABEL, vf_label, VoltageValue.V220)
    # graphic.save(f"data/svg/{vf_label.replace(' ', '_')}.svg")

    nlt = analysis.reading_number(vf_label, VoltageValue.V220)
    drt = analysis.relative_duration_transgress(nlt.nlp, nlt.nlc)
    print(f"nla = {nlt.nla}")
    print(f"nlp = {nlt.nlp}")
    print(f"nlc = {nlt.nlc}")
    print(f"drp = {drt.drp:.2f}%")
    print(f"drc = {drt.drc:.2f}%")


for vl_label in vl_labels:
    print(f"\nIndicadores de variação de tensão para {vl_label}")
    # graphic = analysis.graphic_voltage(TIME_LABEL, vl_label, VoltageValue.V380)
    # graphic.save(f"data/svg/{vl_label.replace(' ', '_')}.svg")

    nlt = analysis.reading_number(vl_label, VoltageValue.V380)
    drt = analysis.relative_duration_transgress(nlt.nlp, nlt.nlc)
    print(f"nla = {nlt.nla}")
    print(f"nlp = {nlt.nlp}")
    print(f"nlc = {nlt.nlc}")
    print(f"drp = {drt.drp:.2f}%")
    print(f"drc = {drt.drc:.2f}%")

print("\nDistorções Harmônicas".center(50))
print("-" * 50)

for voltage_label in voltage_labels:
    print(f"\nIndicadores de Distorções Harmônicas para {voltage_label}")
    harmonic = analysis.harmonic_distortions(harmonics_cols(voltage_label))
    print(f"dtt_95 = {harmonic.dtt_95:.2f}%")
    print(f"dtt_p_95 = {harmonic.dtt_p_95:.2f}%")
    print(f"dtt_i_95 = {harmonic.dtt_i_95:.2f}%")
    print(f"dtt_3_95 = {harmonic.dtt_3_95:.2f}%")

print("\nDesequilíbrio de Tensão".center(50))
print("-" * 50)

fd_95 = analysis.voltage_imbalance("V1_Avg [V]", "V2_Avg [V]", "V3_Avg [V]")
print(f"fd_95 = {fd_95:.2f}%")
