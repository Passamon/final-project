# from re import S
# from scipy.integrate import odeint
# import numpy as np
# import matplotlib.pyplot as plt

# def odes(x, t):
#     # constants
#     beta = 1.11e-9
#     zetas = 0.0002
#     zetah = 0.00015
#     omega1=0.0088
#     omega2=0.0075
#     omega3=0.0085
#     epsilon1=0.641
#     epsilon2=0.704
#     mu=3.6529e-5
#     alpha=0.013
#     lambdas=0.021
#     lambdah=0.0125


#     # assign each ODE to a vector element
#     # S = x[0]
#     # I = x[1]
#     # V1 = x[2]
#     # V2 = x[3]
#     # M = x[4]
#     # H = x[5]
#     # R = x[6]
#     # D = x[7]

#     S = x[0];
#     V1 = x[1];
#     V2 = x[2];
#     I = x[3];
#     R = x[4];
#     H = x[5];
#     M = x[6];
#     D = x[7];

#     # define each ODE
#     dSdt = - beta*S*I - omega1*S - mu*S
#     dV1dt = omega1*S - omega2*V1 - beta*(1-epsilon1)*V1*I - mu*V1
#     dV2dt = omega2*V1 - omega3*V2 - beta*(1-epsilon2)*V2*I - mu*V2
#     dMdt = omega3*V2 + R - beta*(1-epsilon2)*M*I - mu*M
#     dIdt = beta*S*I + beta*(1-epsilon1)*V1*I + beta*(1-epsilon2)*V2*I + beta*(1-epsilon2)*M*I - alpha*I -lambdas*I - zetas*I
#     dHdt = alpha*I - lambdah*I - zetah*H
#     dRdt = lambdas*I + lambdah*H -R
#     dDdt = zetas*I +zetah*H

#     return[dSdt,dV1dt,dV2dt,dIdt,dRdt,dHdt,dMdt,dDdt]



# # innitial conditions
# N = 66186000
# print(N)
# y0=[51001012,13955087,3911439,615314,13402,205002,405322,4990];


# t = np.linspace(0,14,15)
# x = odeint(odes,y0,t)
# print(x)

# # S = x[:,0]
# # I = x[:,1]
# # V1 = x[:,2]
# # V2 = x[:,3]
# # M = x[:,4]
# # H = x[:,5]
# # R = x[:,6]
# # D = x[:,7]



# # plt.semilogy(t,S)
# # plt.semilogy(t,I)
# # plt.semilogy(t,V1)
# # plt.semilogy(t,V2)
# # plt.semilogy(t,M)
# # plt.semilogy(t,H)
# # plt.semilogy(t,R)
# # plt.semilogy(t,D)
# # plt.show()

#     # elif request.method == 'POST':
#     #     start = request.get_json()["start_date"]
        
#     #     defult = query("SELECT beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah FROM public.default WHERE name = \'" + start + "\' LIMIT 1;")

#     #     beta = float(defult[0]["beta"])
#     #     zetas = float(defult[0]["zetas"])
#     #     zetah = float(defult[0]["zetah"])
#     #     omega1 = float(defult[0]["omega1"])
#     #     omega2 = float(defult[0]["omega2"])
#     #     omega3 = float(defult[0]["omega3"])
#     #     epsilon1 = float(defult[0]["epsilon1"])
#     #     epsilon2 = float(defult[0]["epsilon2"])
#     #     mu = float(defult[0]["mu"])
#     #     alpha = float(defult[0]["alpha"])
#     #     lambdas = float(defult[0]["lambdas"])
#     #     lambdah = float(defult[0]["lambdah"])

#     #     date_start = datetime.datetime.strptime(start, "%Y-%m-%d")

#     #     dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase WHERE date = \'" + start + "\' ORDER BY date ASC;")
#     #     vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date = \'" + start + "\' ORDER BY date ASC;")

#     #     x0=[int(dailycase_data[0]["susceptible"]),int(vaccine_data[0]["vaccines1"]),int(vaccine_data[0]["vaccines2"]),int(dailycase_data[0]["infected"]),int(dailycase_data[0]["recovery"]),int(dailycase_data[0]["hospital"]),int(dailycase_data[0]["recovery1"]) + int(vaccine_data[0]["vaccines3"]),int(dailycase_data[0]["deaths"])]
        
#     #     length = 16
#     #     result = []
#     #     result1 = []
#     #     i = 0

#     #     t = np.linspace(0, length - 1, length)
#     #     output = odeint(odes,x0,t)

#     #     for i in range(length):  

#     #         date_1 = date_start + datetime.timedelta(days=i)
#     #         date_string = str(date_1)
#     #         splited_date_string = date_string.split(sep = " ")
            
#     #         result1.append({
#     #             "name": str(splited_date_string[0]), 
#     #             "Susceptible": int(output[i][0]),
#     #             "Infected": int(output[i][3]),
#     #             "Recovery": int(output[i][4]),
#     #             "Hospital": int(output[i][5]),
#     #             "Deaths": int(output[i][7]),
#     #             "Vaccine1": int(output[i][1]),
#     #             "Vaccine2": int(output[i][2]),
#     #             "Maintenance": int(output[i][6]),
#     #             # "test": str(dailycase_data[i]["name"])
#     #         })

#     #         updatecal(str(splited_date_string[0]),int(output[i][0]),int(output[i][1]),int(output[i][2]),int(output[i][3]),int(output[i][4]),int(output[i][5]),int(output[i][7]),int(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')))
    
#     #     print(result1)

            
#     #     result.append({
#     #         "name": str(start),
#     #         "beta": float(defult[0]["beta"]),
#     #         "zetas": float(defult[0]["zetas"]),
#     #         "zetah": float(defult[0]["zetah"]),
#     #         "omega1": float(defult[0]["omega1"]),
#     #         "omega2": float(defult[0]["omega2"]),
#     #         "omega3": float(defult[0]["omega3"]),
#     #         "epsilon1": float(defult[0]["epsilon1"]),
#     #         "epsilon2": float(defult[0]["epsilon2"]),
#     #         "mu": float(defult[0]["mu"]),
#     #         "alpha": float(defult[0]["alpha"]),
#     #         "lambdas": float(defult[0]["lambdas"]),
#     #         "lambdah": float(defult[0]["lambdah"]),
#     #     })
                
#     #     return jsonify({
#     #         "initial_default": result
#     #     })

#     @app.route("/calcovidmodel" , methods=['POST'])
# @cross_origin()
# def calcovidmodel():

#     global beta
#     global zetas
#     global zetah 
#     global omega1
#     global omega2
#     global omega3
#     global epsilon1
#     global epsilon2
#     global mu
#     global alpha
#     global lambdas
#     global lambdah
#     global length

#     # innitial conditions
#     start = request.get_json()["start_date"]

#     initial_value = query("SELECT beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah, length FROM initialvalue WHERE name = \'" + start + "\' ORDER BY date DESC LIMIT 1;")
#     beta = float(initial_value[0]["beta"])
#     zetas = float(initial_value[0]["zetas"])
#     zetah = float(initial_value[0]["zetah"])
#     omega1 = float(initial_value[0]["omega1"])
#     omega2 = float(initial_value[0]["omega2"])
#     omega3 = float(initial_value[0]["omega3"])
#     epsilon1 = float(initial_value[0]["epsilon1"])
#     epsilon2 = float(initial_value[0]["epsilon2"])
#     mu = float(initial_value[0]["mu"])
#     alpha = float(initial_value[0]["alpha"])
#     lambdas = float(initial_value[0]["lambdas"])
#     lambdah = float(initial_value[0]["lambdah"])
#     length = int(initial_value[0]["length"])
    
#     date_start = datetime.datetime.strptime(start, "%Y-%m-%d")
#     # print(int(length))

#     dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase WHERE date = \'" + start + "\' ORDER BY date ASC;")
#     vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date = \'" + start + "\' ORDER BY date ASC;")
    
#     i = 0
#     result = []
    
#     while i < len(dailycase_data):
        

#         x0=[int(dailycase_data[i]["susceptible"]),int(vaccine_data[i]["vaccines1"]),int(vaccine_data[i]["vaccines2"]),int(dailycase_data[i]["infected"]),int(dailycase_data[i]["recovery"]),int(dailycase_data[i]["hospital"]),int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["deaths"])]
        
#         i = i + 1

#     t = np.linspace(0,int(length) - 1,int(length))
#     output = odeint(odes,x0,t)
#     # print(t)
    

#     for i in range(int(length)):  

#         date_1 = date_start + datetime.timedelta(days=i)
#         date_string = str(date_1)
#         splited_date_string = date_string.split(sep = " ")
        
#         result.append({
#             "name": str(splited_date_string[0]), 
#             "Susceptible": int(output[i][0]),
#             "Infected": int(output[i][3]),
#             "Recovery": int(output[i][4]),
#             "Hospital": int(output[i][5]),
#             "Deaths": int(output[i][7]),
#             "Vaccine1": int(output[i][1]),
#             "Vaccine2": int(output[i][2]),
#             "Maintenance": int(output[i][6]),
#             # "test": str(dailycase_data[i]["name"])
#         })

#         updatecal(str(splited_date_string[0]),int(output[i][0]),int(output[i][1]),int(output[i][2]),int(output[i][3]),int(output[i][4]),int(output[i][5]),int(output[i][7]),int(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')))
  
#     # print(result)
#     # return ""
    
#     return jsonify({
#          "data": result
#     })

# @app.route("/coviddata" , methods=['POST'])
# @cross_origin()
# def data():
    
#     start = request.get_json()["start_date"]     
#     end = request.get_json()["end_date"]
    
#     dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, hospitalized as hospital, deaths as deaths, susceptible, recovered as recovery1  FROM dailycase WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
#     vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
    

#     i = 0
#     result = []
    
#     while i < len(dailycase_data):
        
#         date_string = str(dailycase_data[i]["name"])
#         splited_date_string = date_string.split(sep = "-")
        
#         result.append({
#             "name": str(dailycase_data[i]["name"]),
#             "Susceptible": int(dailycase_data[i]["susceptible"]),
#             "Infected": int(dailycase_data[i]["infected"]),
#             "Recovery": int(dailycase_data[i]["recovery"]),
#             "Hospital": int(dailycase_data[i]["hospital"]),
#             "Deaths": int(dailycase_data[i]["deaths"]),
#             "Vaccine1": int(vaccine_data[i]["vaccines1"]),
#             "Vaccine2": int(vaccine_data[i]["vaccines2"]),
#             "Maintenance":int(dailycase_data[i]["recovery1"])+int(vaccine_data[i]["vaccines3"]),
#             # "test": str(dailycase_data[i]["name"])
#         })
            
#         i = i + 1       
    
#     return jsonify({
#          "data": result
#     })