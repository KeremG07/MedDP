import data_preprocessor as dp
import queries as qs
import tkinter as tk
from tkinter import ttk
import matplotlib
from PIL import ImageTk, Image
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

#### READ DATABASE

demographic = dp.read_demographic()
examination = dp.read_examination()
labs = dp.read_labs()

font = {'size'   : 8}
matplotlib.rc('font', **font)
epsilon_budget=2.0


#### QUERY TO CHARTS FUNCTION DEFINITIONS
def AverageExamResultsToBarChartToCanvas(root, demo_title, exam_title):
    averages, fields_result, interval, epsilon = qs.avg_query(demographic, demo_title, examination, exam_title)

    figure = Figure()
    axes = figure.add_subplot()

    if demo_title == "AGE":
        # demo title is age
        y_labels = []
        # construct ranges from lower bounds
        for age in fields_result:
            range_end = age + interval
            y_label = str(int(age)) + " - " + str(int(range_end))
            y_labels.append(y_label)
        # update fields
        fields_result = y_labels

    if demo_title == "GENDER":
        fields_result = ["MALE", "FEMALE"]

    if demo_title == "RACE":
        fields_result = ["HISPANIC", "ASIAN", "WHITE AMERICAN", "WHITE EUROPEAN", "AFRICAN AMERICAN", "MIDDLE EASTERN"]
        axes.set_xticklabels(fields_result, rotation=10)

    axes.bar(fields_result, averages)

    # Axis formatting.
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_color('#DDDDDD')
    axes.tick_params(bottom=False, left=False)
    axes.set_axisbelow(True)
    axes.yaxis.grid(True, color='#EEEEEE')
    axes.xaxis.grid(False)

    axes.set_title(str('Average ' + exam_title + ' of patients grouped by ' + demo_title))
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, height=300, width=500)


def AverageLabResultsToBarChartToCanvas(root, demo_title, lab_title):
    averages, fields_result, interval, epsilon = qs.avg_query(demographic, demo_title, labs, lab_title)

    figure = Figure()
    axes = figure.add_subplot()

    if demo_title == "AGE":
        # demo title is age
        y_labels = []
        # construct ranges from lower bounds
        for age in fields_result:
            range_end = age + interval
            y_label = str(int(age)) + " - " + str(int(range_end))
            y_labels.append(y_label)
        # update fields
        fields_result = y_labels

    if demo_title == "GENDER":
        fields_result = ["MALE", "FEMALE"]

    if demo_title == "RACE":
        fields_result = ["HISPANIC", "ASIAN", "WHITE AMERICAN", "WHITE EUROPEAN", "AFRICAN AMERICAN", "MIDDLE EASTERN"]
        axes.set_xticklabels(fields_result, rotation=10)

    axes.bar(fields_result, averages)

    # Axis formatting.
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_color('#DDDDDD')
    axes.tick_params(bottom=False, left=False)
    axes.set_axisbelow(True)
    axes.yaxis.grid(True, color='#EEEEEE')
    axes.xaxis.grid(False)

    axes.set_title(str('Average ' + lab_title + ' of patients grouped by ' + demo_title))
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, height=300, width=500)


def DistributionBasedOnRaceAndGenderToPieChartToCanvas(root, exam_lab_title, race_title, gend_title):
    if exam_lab_title in ["PULSE", "BMI", "WEIGHT", "HEIGHT"]:
        dataset_group_by = examination
    if exam_lab_title in ["CALCIUM", "CHOLESTEROL", "PROTEIN", "URIC_ACID", "HEMOGLOBIN"]:
        dataset_group_by = labs

    gend_title_to_int = 0
    race_title_to_int = 0

    if gend_title == "MALE":
        gend_title_to_int = 1
    elif gend_title == "FEMALE":
        gend_title_to_int = 2

    if race_title == "HISPANIC":
        race_title_to_int = 1
    elif race_title == "ASIAN":
        race_title_to_int = 2
    elif race_title == "WHITE AMERICAN":
        race_title_to_int = 3
    elif race_title == "WHITE EUROPEAN":
        race_title_to_int = 4
    elif race_title == "AFRICAN AMERICAN":
        race_title_to_int = 6
    elif race_title == "MIDDLE EASTERN":
        race_title_to_int = 7

    if race_title == "ANY" and gend_title != "ANY":
        counts, fields_result, interval = qs.single_constraint_query(dataset_group_by, exam_lab_title, demographic, "GENDER", gend_title_to_int)
    elif race_title != "ANY" and gend_title == "ANY":
        counts, fields_result, interval = qs.single_constraint_query(dataset_group_by, exam_lab_title, demographic, "RACE", race_title_to_int)
    elif race_title == "ANY" and gend_title == "ANY":
        counts, fields_result, interval = qs.general_count_query(dataset_group_by, exam_lab_title)
    else:
        counts, fields_result, interval = qs.double_constraint_query(dataset_group_by, exam_lab_title, demographic, "RACE", "GENDER", race_title_to_int, gend_title_to_int)
    
    fields_result = [ round(field, 2) for field in fields_result ]

    figure = Figure()
    axes = figure.add_subplot()

    print(counts, fields_result)

    axes.pie(counts, labels=fields_result, autopct='%1.1f%%',
        shadow=True, startangle=90)
    axes.axis('equal')

    axes.set_title(str('Distribution of ' + exam_lab_title + ' among patients who are ' + race_title + " and " + gend_title))
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, height=300, width=500)


def DistributionBasedOnAgeRangeToPieChartToCanvas(root, exam_lab_title, age_lowerb, age_upperb):
    if not (int(age_lowerb) < int(age_upperb)):
        return
    
    if exam_lab_title in ["PULSE", "BMI", "WEIGHT", "HEIGHT"]:
        dataset_group_by = examination
    if exam_lab_title in ["CALCIUM", "CHOLESTEROL", "PROTEIN", "URIC_ACID", "HEMOGLOBIN"]:
        dataset_group_by = labs
    counts, fields_result, interval = qs.age_range_query(dataset_group_by, exam_lab_title, int(age_lowerb), int(age_upperb))

    fields_result = [ round(field, 2) for field in fields_result ]

    figure = Figure()
    axes = figure.add_subplot()

    axes.pie(counts, labels=fields_result, autopct='%1.1f%%',
        shadow=True, startangle=90)
    axes.axis('equal')

    axes.set_title(str('Distribution of ' + exam_lab_title + ' among patients aged between ' + age_lowerb + " and " + age_upperb))
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, height=300, width=500)


def BidirectionalAverageExamAndLabResultsToBidirectionalBarChartToCanvas(root, exam_lab_title):
    if exam_lab_title in ["PULSE", "BMI", "WEIGHT", "HEIGHT"]:
        dataset_group_by = examination
    if exam_lab_title in ["CALCIUM", "CHOLESTEROL", "PROTEIN", "URIC_ACID", "HEMOGLOBIN"]:
        dataset_group_by = labs
    avg, fields_result, interval = qs.avg_bi_histogram_query(dataset_group_by, exam_lab_title)

    figure = Figure()
    axes = figure.add_subplot()

    ## invert opposite gender data for visuals
    opposite_avg = []
    for data in avg[1]:
        opposite_avg.append(-data)

    axes.barh(fields_result, avg[0], color = 'r')
    axes.barh(fields_result, opposite_avg, color = 'b')

    # Axis formatting.
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_color('#DDDDDD')
    axes.tick_params(bottom=False, left=False)
    axes.set_axisbelow(True)
    axes.yaxis.grid(True, color='#EEEEEE')
    axes.xaxis.grid(False)

    axes.set_title("Bidirectional " + exam_lab_title + " Data of MALE and FEMALE patiens grouped by AGE")
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=150, height=300, width=500)


#### WINDOW

root = tk.Tk()
root.title("MedDP")
root.resizable = (False, False)
root.geometry('950x650')

frame = tk.Frame(root, width=811, height=165)
frame.pack()
frame.place(x=400, y=20)
img = ImageTk.PhotoImage(Image.open("meddp-logo.gif").resize((500, 100)))
label = tk.Label(frame, image = img)
label.pack()

## QUERY FIELD CONSTRUCTORS

exam_titles = ["PULSE", "BMI", "WEIGHT", "HEIGHT"]
lab_titles = ["CALCIUM", "CHOLESTEROL", "PROTEIN", "URIC_ACID", "HEMOGLOBIN"]
exam_lab_titles = ["PULSE", "BMI", "WEIGHT", "HEIGHT", "CALCIUM", "CHOLESTEROL", "PROTEIN", "URIC_ACID", "HEMOGLOBIN"]
demo_titles = ["AGE", "RACE", "GENDER"]

gend_titles = ["ANY", "MALE", "FEMALE"]
race_titles = ["ANY", "HISPANIC", "ASIAN", "WHITE AMERICAN", "WHITE EUROPEAN", "AFRICAN AMERICAN", "MIDDLE EASTERN"]
age_titles = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]

avg_exam_var = tk.StringVar(root)
avg_exam_var.set(exam_titles[0])
avg_exam_dwn = tk.OptionMenu(root, avg_exam_var, *exam_titles)
avg_exam_dwn.config(width=len(max(exam_lab_titles, key=len)))
avg_exam_demo_var = tk.StringVar(root)
avg_exam_demo_var.set(demo_titles[0])
avg_exam_demo_dwn = tk.OptionMenu(root, avg_exam_demo_var, *demo_titles)
avg_exam_demo_dwn.config(width=len(max(exam_lab_titles, key=len)))
avg_exam_demo_btn = ttk.Button(root, text="Perform Query", command=lambda:AverageExamResultsToBarChartToCanvas(root, avg_exam_demo_var.get(), avg_exam_var.get()))
avg_exam_demo_btn.config(width=len(max(exam_lab_titles, key=len)))

avg_lab_var = tk.StringVar(root)
avg_lab_var.set(lab_titles[0])
avg_lab_dwn = tk.OptionMenu(root, avg_lab_var, *lab_titles)
avg_lab_dwn.config(width=len(max(exam_lab_titles, key=len)))
avg_lab_demo_var = tk.StringVar(root)
avg_lab_demo_var.set(demo_titles[0])
avg_lab_demo_dwn = tk.OptionMenu(root, avg_lab_demo_var, *demo_titles)
avg_lab_demo_dwn.config(width=len(max(exam_lab_titles, key=len)))
avg_lab_demo_btn = ttk.Button(root, text="Perform Query", command=lambda:AverageLabResultsToBarChartToCanvas(root, avg_lab_demo_var.get(), avg_lab_var.get()))
avg_lab_demo_btn.config(width=len(max(exam_lab_titles, key=len)))

dist_exam_lab_var = tk.StringVar(root)
dist_exam_lab_var.set(exam_lab_titles[0])
dist_exam_lab_dwn = tk.OptionMenu(root, dist_exam_lab_var, *exam_lab_titles)
dist_exam_lab_dwn.config(width=len(max(exam_lab_titles, key=len)))
dist_race_var = tk.StringVar(root)
dist_race_var.set(race_titles[0])
dist_race_dwn = tk.OptionMenu(root, dist_race_var, *race_titles)
dist_race_dwn.config(width=len(max(exam_lab_titles, key=len)))
dist_gend_var = tk.StringVar(root)
dist_gend_var.set(gend_titles[0])
dist_gend_dwn = tk.OptionMenu(root, dist_gend_var, *gend_titles)
dist_gend_dwn.config(width=len(max(exam_lab_titles, key=len)))
dist_race_gend_btn = ttk.Button(root, text="Perform Query", command=lambda:DistributionBasedOnRaceAndGenderToPieChartToCanvas(root, dist_exam_lab_var.get(), dist_race_var.get(), dist_gend_var.get()))
dist_race_gend_btn.config(width=len(max(exam_lab_titles, key=len)))

dist_age_lowerb_var = tk.StringVar(root)
dist_age_lowerb_var.set(age_titles[0])
dist_age_lowerb_dwn = tk.OptionMenu(root, dist_age_lowerb_var, *age_titles)
dist_age_lowerb_dwn.config(width=len(max(exam_lab_titles, key=len)))
dist_age_upperb_var = tk.StringVar(root)
dist_age_upperb_var.set(age_titles[len(age_titles)-1])
dist_age_upperb_dwn = tk.OptionMenu(root, dist_age_upperb_var, *age_titles)
dist_age_upperb_dwn.config(width=len(max(exam_lab_titles, key=len)))
dist_age_btn = ttk.Button(root, text="Perform Query", command=lambda:DistributionBasedOnAgeRangeToPieChartToCanvas(root, dist_exam_lab_var.get(), dist_age_lowerb_var.get(), dist_age_upperb_var.get()))
dist_age_btn.config(width=len(max(exam_lab_titles, key=len)))

bid_exam_lab_var = tk.StringVar(root)
bid_exam_lab_var.set(exam_lab_titles[0])
bid_exam_lab_dwn = tk.OptionMenu(root, bid_exam_lab_var, *exam_lab_titles)
bid_exam_lab_dwn.config(width=len(max(exam_lab_titles, key=len)))
bid_exam_lab_btn = ttk.Button(root, text="Perform Query", command=lambda:BidirectionalAverageExamAndLabResultsToBidirectionalBarChartToCanvas(root, bid_exam_lab_var.get()))
bid_exam_lab_btn.config(width=len(max(exam_lab_titles, key=len)))

## GRID PLACEMENT

tk.Label(root, text="AVERAGE EXAM RESULTS", font=("Helvetica 12 bold")).grid(row = 0, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="Average").grid(row = 1, column = 0, sticky = 'w', padx = 5, pady = 2)
avg_exam_dwn.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="of patients grouped by").grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 2)
avg_exam_demo_dwn.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 2)
avg_exam_demo_btn.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 2)

tk.Label(root, text="AVERAGE LAB RESULTS", font=("Helvetica 12 bold")).grid(row = 4, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="Average").grid(row = 5, column = 0, sticky = 'w', padx = 5, pady = 2)
avg_lab_dwn.grid(row = 5, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="of patients grouped by").grid(row = 6, column = 0, sticky = 'w', padx = 5, pady = 2)
avg_lab_demo_dwn.grid(row = 6, column = 1, sticky = 'w', padx = 5, pady = 2)
avg_lab_demo_btn.grid(row = 7, column = 1, sticky = 'w', padx = 5, pady = 2)

tk.Label(root, text="DISTRIBUTION OF EXAM & LAB RESULTS", font=("Helvetica 12 bold")).grid(row = 8, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="Distribution of").grid(row = 9, column = 0, sticky = 'w', padx = 5, pady = 2)
dist_exam_lab_dwn.grid(row = 9, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="    BASED ON RACE AND GENDER", font=("Helvetica 12 bold")).grid(row = 10, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="    of patients who are").grid(row = 11, column = 0, sticky = 'w', padx = 5, pady = 2)
dist_race_dwn.grid(row = 11, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="    and").grid(row = 12, column = 0, sticky = 'w', padx = 5, pady = 2)
dist_gend_dwn.grid(row = 12, column = 1, sticky = 'w', padx = 5, pady = 2)
dist_race_gend_btn.grid(row = 13, column = 1, sticky = 'w', padx = 5, pady = 2)

tk.Label(root, text="    BASED ON AGE RANGE", font=("Helvetica 12 bold")).grid(row = 14, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="    aged between").grid(row = 15, column = 0, sticky = 'w', padx = 5, pady = 2)
dist_age_lowerb_dwn.grid(row = 15, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="    and").grid(row = 16, column = 0, sticky = 'w', padx = 5, pady = 2)
dist_age_upperb_dwn.grid(row = 16, column = 1, sticky = 'w', padx = 5, pady = 2)
dist_age_btn.grid(row = 17, column = 1, sticky = 'w', padx = 5, pady = 2)

tk.Label(root, text="BIDIRECTIONAL AVERAGE EXAM & LAB RESULTS", font=("Helvetica 12 bold")).grid(row = 18, column = 0, sticky= 'w', padx = 5, pady = 2, columnspan=2)
tk.Label(root, text="Distribution of").grid(row = 19, column = 0, sticky = 'w', padx = 5, pady = 2)
bid_exam_lab_dwn.grid(row = 19, column = 1, sticky = 'w', padx = 5, pady = 2)
tk.Label(root, text="over AGE and GENDER groups").grid(row = 20, column = 0, sticky = 'w', padx = 5, pady = 2)
bid_exam_lab_btn.grid(row = 21, column = 1, sticky = 'w', padx = 5, pady = 2)

## END GRID PLACEMENT

root.mainloop()