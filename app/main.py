from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


RECITATION_HOURS = {"a": "09:00~09:50", "b": "10:00~10:50",
                    "c": "11:00~11:50", "d": "12:00~12:50"}
MICROSERVICE_LINK = "https://whos-my-ta.fly.dev/section_id/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get("https://whos-my-ta.fly.dev/section_id/" + section_id)

    # You can check out what the response body looks like in terminal using the print statement
    data = response.json()
    print(data)
    ta_name_list = data["ta_names"]
    ta1_name = ta_name_list[0]["fname"] + " " + ta_name_list[0]["lname"]
    ta2_name = ta_name_list[1]["fname"] + " " + ta_name_list[1]["lname"]

    print(ta1_name)

    # TODO
    if section_id == "a" or section_id == "b" or section_id == "c" or section_id == "d" :
        time = RECITATION_HOURS[section_id]
        times_split = time.split("~")
        start = times_split[0]
        end = times_split[1]
        return {
            "section": section_id,
            "start_time": start,
            "end_time": end,
            "ta": [ta1_name, ta2_name]
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
