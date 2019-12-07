import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("10k_dw_700_cm.csv")
data["ICSJ"] = data["Init_Time"] + data["Comp_Time"] + data["Scatter_Time"] + data["Join_Time"]

# Init

init_data = data[data["SS"]==0][["Query", "Split", "SS", "IV", "AV", "Init_Time"]].groupby(["Query", "Split", "SS"]).agg({"IV": max, "AV": max, "Init_Time": max})
init_x = init_data[["IV", "AV"]]
init_y = init_data[["Init_Time"]]
init_x = sm.add_constant(init_x)
init_model = sm.OLS(init_y, init_x).fit()
init_model.save("init_model.mdl")

# Compute

comp_data = data[data["SS"]!=0][["Query", "Split", "SS", "IV", "AV", "Input_Msg_Count", "Comp_Time"]].groupby(["Query", "Split", "SS"]).agg({"IV": max, "AV": max, "Comp_Time": max, "Input_Msg_Count": max})
comp_x = comp_data[["IV", "AV", "Input_Msg_Count"]]
comp_y = comp_data[["Comp_Time"]]
comp_x = sm.add_constant(comp_x)
comp_model = sm.OLS(comp_y, comp_x).fit()
comp_model.save("comp_model.mdl")


# Scatter

scat_data = data[data["IE"]!=0][["Query", "Split", "SS", "IE", "Scatter_Time"]].groupby(["Query", "Split", "SS"]).agg({"IE": max, "Scatter_Time": max})
scat_x = scat_data[["IE"]]
scat_y = scat_data[["Scatter_Time"]]
scat_x = sm.add_constant(scat_x)
scat_model = sm.OLS(scat_y, scat_x).fit()
scat_model.save("scat_model.mdl")


# Join

join_data = data[data["Join_Count"]!=0][["Query", "Split", "SS", "Join_Count", "left_cross_right", "Join_Time"]].groupby(["Query", "Split", "SS"]).agg({"Join_Count": max, "left_cross_right": max, "Join_Time": max})
join_x = join_data[["Join_Count", "left_cross_right"]]
join_y = join_data[["Join_Time"]]
join_x = sm.add_constant(join_x)
join_model = sm.OLS(join_y, join_x).fit()
join_model.save("join_model.mdl")


# Interval Compute

ic_x = data[["ICSJ", "Total_Comp_Count"]]
ic_y = data["Tot_Comp_Time"]
ic_x = sm.add_constant(ic_x)
ic_model = sm.OLS(ic_y, ic_x).fit()
ic_model.save("ic_model.mdl")

# SS Time

ss_x = data[["Tot_Comp_Time", "Total_Comp_Count"]]
ss_y = data["Total_SS_Time"]
ss_x = sm.add_constant(ss_x)
ss_model = sm.OLS(ss_y, ss_x).fit()
ss_model.save("ss_model.mdl")


