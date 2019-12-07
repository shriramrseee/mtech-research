import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("100k_f_500_cm.csv")
# data = pd.read_csv("dec-01/10k_dw_700_cm.csv")
data["ICSJ"] = data["Init_Time"] + data["Comp_Time"] + data["Scatter_Time"] + data["Join_Time"]

# Load Models

init_model = sm.load("init_model.mdl")
comp_model = sm.load("comp_model.mdl")
scat_model = sm.load("scat_model.mdl")
join_model = sm.load("join_model.mdl")
ic_model = sm.load("ic_model.mdl")
ss_model = sm.load("ss_model.mdl")

# init_model = sm.load("dec-01/init_model.mdl")
# comp_model = sm.load("dec-01/comp_model.mdl")
# scat_model = sm.load("dec-01/scat_model.mdl")
# join_model = sm.load("dec-01/join_model.mdl")
# ic_model = sm.load("dec-01/ic_model.mdl")
# ss_model = sm.load("dec-01/ss_model.mdl")

# Prepare Input

# Init

init_data = data[data["SS"]==0][["Query", "Split", "SS", "IV", "AV", "Init_Time"]].groupby(["Query", "Split", "SS"]).agg({"IV": max, "AV": max, "Init_Time": max})
init_x = init_data[["IV", "AV"]]
init_y = init_data[["Init_Time"]]
init_x = sm.add_constant(init_x)
init_y_pred = init_model.predict(init_x)

# Compute

comp_data = data[data["SS"]!=0][["Query", "Split", "SS", "IV", "AV", "Input_Msg_Count", "Comp_Time"]].groupby(["Query", "Split", "SS"]).agg({"IV": max, "AV": max, "Comp_Time": max, "Input_Msg_Count": max})
comp_x = comp_data[["IV", "AV", "Input_Msg_Count"]]
comp_y = comp_data[["Comp_Time"]]
comp_x = sm.add_constant(comp_x)
comp_y_pred = comp_model.predict(comp_x)

# Scatter

scat_data = data[data["IE"]!=0][["Query", "Split", "SS", "IE", "Scatter_Time"]].groupby(["Query", "Split", "SS"]).agg({"IE": max, "Scatter_Time": max})
scat_x = scat_data[["IE"]]
scat_y = scat_data[["Scatter_Time"]]
scat_x = sm.add_constant(scat_x)
scat_y_pred = scat_model.predict(scat_x)

# Join

join_data = data[data["Join_Count"]!=0][["Query", "Split", "SS", "Join_Count", "left_cross_right", "Join_Time"]].groupby(["Query", "Split", "SS"]).agg({"Join_Count": max, "left_cross_right": max, "Join_Time": max})
join_x = join_data[["Join_Count", "left_cross_right"]]
join_y = join_data[["Join_Time"]]
join_x = sm.add_constant(join_x)
join_y_pred = join_model.predict(join_x)

# Interval Compute

ic_x_t = pd.merge(init_y_pred.to_frame("I"), comp_y_pred.to_frame("C"), on=["Query", "Split", "SS"], how="outer")
ic_x_t = pd.merge(ic_x_t, scat_y_pred.to_frame("S"), on=["Query", "Split", "SS"], how="outer")
ic_x_t = pd.merge(ic_x_t, join_y_pred.to_frame("J"), on=["Query", "Split", "SS"], how="outer")
ic_x_t = ic_x_t.fillna(0)
# ic_x_t.to_csv("debug.csv")
ic_x = (ic_x_t["I"] + ic_x_t["C"] + ic_x_t["S"] + ic_x_t["J"]).to_frame("ICSJ")
ic_x = pd.merge(ic_x, data[["Query", "Split", "SS", "Total_Comp_Count"]].groupby(["Query", "Split", "SS"]).agg({"Total_Comp_Count": max}), on=["Query", "Split", "SS"], how="outer")
ic_y = data["Tot_Comp_Time"]
ic_x = sm.add_constant(ic_x)
ic_y_pred = ic_model.predict(ic_x)


# SS Time

ss_x = pd.merge(ic_y_pred.to_frame("Tot_Comp_Time"), data[["Query", "Split", "SS", "Total_Comp_Count"]].groupby(["Query", "Split", "SS"]).agg({"Total_Comp_Count": max}), on=["Query", "Split", "SS"], how="outer")
ss_y = data["Total_SS_Time"]
ss_x = sm.add_constant(ss_x)
ss_y_pred = ss_model.predict(ss_x)

# Save to file

output = pd.merge(ss_y_pred.to_frame("Pred_Total_SS_Time"), data[["Query", "Split", "SS", "Type", "Total_SS_Time"]].groupby(["Query", "Split", "SS"]).agg({"Total_SS_Time": max, "Type": max}), on=["Query", "Split", "SS"], how="outer")
output = output.groupby(["Query", "Type", "Split"]).agg({"Total_SS_Time": sum, "Pred_Total_SS_Time": sum})
output.to_csv("100k_f_500_ac_evaluate.csv")