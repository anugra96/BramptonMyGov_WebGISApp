import pandas as pd
import numpy as np
import geopandas as gpd
import fiona



def make_geojson(code):
    print(code)
    ## import raw votes csv data from open data
    votes_raw = pd.read_csv("https://raw.opendata.arcgis.com/datasets/d730fdb5345648b4abb3084f82dbabc4_4.csv?outSR=%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D")

    ## filter covid votes into a new df
    # covid_votes = votes_raw[votes_raw.AGENDA_ITEM_SUBJECT == "COVID-19 Emergency"]
    # covid_votes_df = pd.DataFrame(covid_votes)

    votes_melted = pd.melt(votes_raw, 
                        id_vars=["OBJECTID", "COUNCIL_COMMITTEE", "AGENDA_ITEM_SUBJECT", "RESOLUTION_NUM", "MOTION_DESCRIPTION", "MEETING_DATE", "MINUTE_LINK", "RECORDED_VOTE", "RESULT" ], 
                        value_vars=["BOWMAN", "BROWN", "DHILLON", "FORTINI", "MEDEIROS", "PALLESCHI", "SANTOS", "SINGH", "VINCENTE", "WHILLANS", "WILLIAMS"],
                        var_name="city_councillor",
                        value_name="vote")


    selection_df = votes_melted[votes_melted.RESOLUTION_NUM == code]

    select_first = selection_df.head(1)

    final_output = select_first[[
        "COUNCIL_COMMITTEE", 
        "AGENDA_ITEM_SUBJECT", 
        "MOTION_DESCRIPTION", 
        "MEETING_DATE", 
        "RECORDED_VOTE", 
        "RESULT", 
        "RESOLUTION_NUM", 
        "MINUTE_LINK"]]

    final_output.columns=["COUNCIL", 
                        "MOTION SUBJECT",
                        "MOTION DESCRIPTION",
                        "MEETING_DATE",
                        "RECORDED VOTES", 
                        "RESULT",
                        "RESOLUTION #",
                        "LINK TO MEETING MINUTES"
                        ]


    final_output.to_csv("./static/motion_info.csv", index=False)

    ## import councillor ward csv data for reference
    wards = pd.read_csv("./data/ward_councillors.csv")


    join_1 = pd.merge(wards, selection_df[['city_councillor', 'vote']], how='left', left_on=["councillor_x"], right_on=["city_councillor"])
    join_2 = pd.merge(join_1, selection_df[['city_councillor', 'vote']], how='left', left_on=["councillor_y"], right_on=["city_councillor"])
    join_2


    final_merged_df = join_2[["ward_num", "city_councillor_x", "city_councillor_y", "vote_x", "vote_y", "councillor_x_img", "councillor_y_img", "councillor_x_full_name", "councillor_y_full_name", "councillor_x_email", "councillor_y_email", "councillor_x_phone", "councillor_y_phone"]]
    final_merged_df.set_index("ward_num")


    ## import wards shapefile as geodataframe
    ward_gdf = gpd.read_file("https://opendata.arcgis.com/datasets/61b3e12fb4d74d078a15512dc3baf568_3.geojson")
    print(type(ward_gdf))

    ward_gdf = ward_gdf.rename(columns={"WARD": "ward_num"})
    ward_gdf["ward_num"] = ward_gdf["ward_num"].str.replace("WARD ", "")
    ward_gdf["ward_num"] = ward_gdf["ward_num"].astype(int)
    # print(ward_gdf)

    merged_gdf = ward_gdf.merge(final_merged_df, on="ward_num")
    # print(merged_gdf)


    ## classify the two votes for each ward
    def classify_this(row):
        ret_val = ""
        if ((row['vote_x'] == "Yes") & (row['vote_y'] == "Yes")):
            ret_val = "Yes-Yes"
        elif ((row['vote_x'] == "No") & (row['vote_y'] == "No")):
            ret_val = "No-No"
        elif (((row['vote_x'] == "Yes") & (row['vote_y'] == "No")) | ((row['vote_x'] == "No") & (row['vote_y'] == "Yes"))):
            ret_val = "Yes-No"
        elif (((row['vote_x'] == "Yes") & (row['vote_y'] == "Absent")) | ((row['vote_x'] == "Absent") & (row['vote_y'] == "Yes"))):
            ret_val = "Yes-Absent"
        elif (((row['vote_x'] == "No") & (row['vote_y'] == "Absent")) | ((row['vote_x'] == "Absent") & (row['vote_y'] == "No"))):
            ret_val = "No-Absent"
        else:
            ret_val = "Absent-Absent"
            
        return ret_val

    merged_gdf['final_vote'] = merged_gdf.apply(lambda row: classify_this(row), axis=1)
    ## print(merged_gdf)

    merged_gdf.to_crs("EPSG:4326")

    with open('./static/result.geojson', 'w') as f:
        f.write(merged_gdf.to_json())

    # with open('./static/' + code + '.geojson', 'w') as f:
    #     f.write(merged_gdf.to_json())
    print(code)
    print("done")








