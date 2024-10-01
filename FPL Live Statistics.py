
'''Program displaying Fantasy Premier League (FPL) Statistics for 
the current season. The objective of this project was to create a 
tool that aids users in making data-driven decisions when drafting 
players for their fantasy sports teams.'''

# Importing required libraries
import requests
from tkinter import messagebox
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tabulate import tabulate

    
def result_window(fpl_df,window):
    '''Function to show result'''
    result_window = tk.Toplevel(window)
    result_window.title("Result")
    
    #window dimension and position for geometry
    result_window.geometry("1200x500")    
    
    scrollbar = tk.Scrollbar(result_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Assuming 'df' is your DataFrame
    data = tabulate(fpl_df, headers='keys', tablefmt='psql')
    
    result_text = tk.Text(
        result_window,
        wrap = tk.NONE,
        yscrollcommand=scrollbar.set,
        bg = "black",
        fg = "white"
        )
    result_text.pack(side=tk.LEFT, fill=tk.BOTH,
        expand = True)
    scrollbar.config(command=result_text.yview)
    result_text.insert(tk.END, data)
 

def fpl_stats(position, team, window):
    '''Function which gets the current season fpl stats'''
    # base url for all FPL API endpoints
    base_url = 'https://fantasy.premierleague.com/api/'
    
    # get data from bootstrap-static endpoint
    r = requests.get(base_url+'bootstrap-static/').json()
    
    pd.set_option('display.max_columns', None)
    # create players dataframe
    players = pd.json_normalize(r['elements'])
    
    # create teams dataframe
    teams = pd.json_normalize(r['teams'])
    
    # get position information from 'element_types' field
    positions = pd.json_normalize(r['element_types'])
    
    # join players to teams
    fpl_df = pd.merge(
        left = players,
        right = teams,
        left_on ='team',
        right_on ='id'
    )
    
    
    # join player positions
    fpl_df = fpl_df.merge(
        positions,
        left_on='element_type',
        right_on='id'
    )
    
    
    fpl_df = fpl_df[
        [
            "web_name",
            "now_cost",
            "plural_name_short", 
            "name", 
            "total_points", 
            "goals_scored", 
            "assists", 
            "clean_sheets"
        ]
    ]
    
    fpl_df["now_cost"] = (fpl_df["now_cost"])/10 
    
    fpl_df = fpl_df.rename(
        columns={
            "web_name" : "Player Name",
            "now_cost" : "Cost (£) \n (in millions)",
            "plural_name_short" : "Player Position",
            "name" : "Team Name", 
            "total_points" : "Total Points", 
            "goals_scored" : "Goals Scored", 
            "assists" : "Assists", 
            "clean_sheets" : "Clean Sheets" 
        }
    )
    position_dict = {
        "1" : "GKP",
        "2" : "DEF",
        "3" : "MID",
        "4" : "FWD"
    }
    if position == "Default":
        messagebox.showerror("ERROR", f"Please select a position")
    elif position != "0":
        filteration_1_fpl_df = fpl_df.loc[fpl_df["Player Position"] == position_dict[position]]
    else :
        filteration_1_fpl_df = fpl_df
    if team != "All":
        filteration_2_fpl_df = filteration_1_fpl_df.loc[filteration_1_fpl_df["Team Name"] == team]
    else:
        filteration_2_fpl_df = filteration_1_fpl_df
    
    result_window(filteration_2_fpl_df, window)
    
def fpl_stats_window():
    ''' GUI Main window for input prompts'''

    #Beginning
    input_window = tk.Tk()
    input_window.title("FPL Stats")
    input_window.geometry("500x400")
    input_window.configure(bg = "white")
        
    #Middle
    
        
    #Title Label and Frame
    input_title_frame = tk.Frame(input_window)
    input_title_frame.configure(bg = "white")
    input_title_frame.pack()
    input_title = tk.Label(
        input_title_frame,
        text = "FPL PLAYER STATS - LIVE",
        fg = "darkblue",
        bg = "white",
        font = ("Helvetica", 18, "bold")
        )
    input_title.grid(pady = (50,0))
    
    #positon label
    position_frame = tk.Frame(input_window)
    position_frame.configure(bg = "white")
    position_frame.pack()
    
    position_label = tk.Label(
        position_frame,
        text = "POSITION",
        fg = "midnightblue",
        bg = "white",
        font = ("Helvetica", 12)        
    )
    position_label.grid(padx = (0,0), pady =(50,10))
    
    #Radio Button frame
    position_button_frame = tk.Frame(input_window)
    position_button_frame.configure(bg = "white")
    position_button_frame.pack()
    
    positon_var = tk.StringVar()
    positon_var.set("Default")
    
    every = tk.Radiobutton(
        position_button_frame,
        text = "ALL",
        variable = positon_var,
        value = 0
    )
    every.grid(row = 1)
    
    gk = tk.Radiobutton(
        position_button_frame,
        text = "GK",
        variable = positon_var,
        value = 1
    )
    gk.grid(row = 1, column = 1)
    defr = tk.Radiobutton(
        position_button_frame,
        text = "DEF",
        variable = positon_var,
        value = 2
    )
    defr.grid(row = 1, column = 2)
    
    mid = tk.Radiobutton(
        position_button_frame,
        text = "MID",
        variable = positon_var,
        value = 3
    )
    mid.grid(row = 1, column = 3) 
    
    fwd = tk.Radiobutton(
        position_button_frame,
        text = "FWD",
        variable = positon_var,
        value = 4
    )
    fwd.grid(row = 1, column = 4)

    #Team label and frame
    team_frame = tk.Frame(input_window)
    team_frame.configure(bg = "white")
    team_frame.pack()
    
    dropdown_option = [
        'All','Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
        'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
        'Liverpool', 'Luton', 'Man City', 'Man Utd', 'Newcastle',
        "Nott'm Forest", 'Sheffield Utd', 'Spurs', 'West Ham', 'Wolves'
    ]    
    selected_option = tk.StringVar()
    selected_option.set(dropdown_option[0])
    
    input_team = tk.Label(
        team_frame,
        text = "TEAM",
        fg = "midnightblue",
        bg = "white",
        font = ("Helvetica", 12)        
        )
    input_team.grid(row = 1, pady = (10,10))
    input_team_dropdown = ttk.Combobox(
        team_frame,
        textvariable = selected_option,
        values = dropdown_option
    )
    input_team_dropdown.grid(row = 2, pady = (10,10))
    
    button_frame = tk.Frame(input_window)
    button_frame.configure(bg = "white")
    button_frame.pack()
    
    command_fpl = lambda: fpl_stats(
        positon_var.get(), 
        selected_option.get(), 
        input_window
    )
    
    enter_button = tk.Button(
        button_frame,
        text = "ENTER",
        command = command_fpl
        )
    enter_button.grid(pady = (10,10))    
    
    #End
    input_window.mainloop()

    
fpl_stats_window()
