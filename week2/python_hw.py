# Task 1
def find_and_print(messages, current_station):
    # Define the Green Line including Xiaobitan
    green_line_stations = [
        "Songshan", "Nanjing", "Taipei Arena", "Nanjing Fuxing", "Songjiang Nanjing", "Zhongshan",
        "Beimen", "Ximen", "Xiaonamen", "Chiang Kai-Shek Memorial Hall", "Guting", "Taipower Building",
        "Gongguan", "Wanlong", "Jingmei", "Dapinglin", "Qizhang", "Xindian City Hall", "Xindian"
    ]
    lightgreen_line_station = ["Xiaobitan"]

    people_stations = {}
    people_index = {}

    for person, message in messages.items():
        for station in green_line_stations + lightgreen_line_station:
            if station in message:
                people_stations[person] = station
                if station == "Xiaobitan":
                    people_index[person] = 16.5 # regards "Xiaobitan" as 16.5 according to "Qizhang" is 16
                else:    
                    people_index[person] = green_line_stations.index(station)
                break

    # print(people_stations)
    # print(people_index)

    # For special handling about current_station =="Xiaobitan"
    if current_station =="Xiaobitan":
        current_index = 16.5
    else:    
        current_index = green_line_stations.index(current_station)
    # For specail handling 
    if current_station =="Xindian City Hall":
        current_index+=1
    elif current_station == "Xindian":
        current_index+=2

    # Find the closest person
    closest_person = []
   
    # For only one person in a station
    # min_value=len(green_line_stations)
    # for person, index in people_index.items():
    #     value = abs(current_index-index)
    #     if value<min_value:
    #         min_value = value
    #         closest_person = person
    # print(closest_person)

    # closest_person = min(people_index, key=lambda person: abs(current_index - people_index[person]))
    # print(closest_person)

    # considering about not only one person in the same station
    min_value=len(green_line_stations)
    for person, index in people_index.items():
        value = abs(current_index-index)
        if value<min_value:
            min_value = value
            closest_person = [person]
        elif value==min_value:
            closest_person.append(person)

    if len(closest_person) > 1:
        people = ", ".join(closest_person)
        print(people)
    else:
        print(closest_person[0]) 

    # min_distance = min(abs(current_index - index) for index in people_index.values())
    # closest_person = [person for person, index in people_index.items() if abs(current_index - index) == min_distance]


messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Vivian": "I'm at Xindian station waiting for you.",
}

print("=== TASK 1 ===")
find_and_print(messages, "Wanlong")  # Expected: Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang")  # Expected: Leslie
find_and_print(messages, "Ximen")  # Expected: Bob
find_and_print(messages, "Xindian City Hall")  # Expected: Vivian


# Task 2
bookings = {}

def book(consultants, hour, duration, criteria):
# your code here
    best_consultant = None
    best_value = None

    for consultant in consultants:
        # print(bookings)
        if consultant['name'] in bookings:
            is_booked = False
            for start, end in bookings[consultant['name']]:
                if not (hour + duration <= start or hour >= end):
                    is_booked = True
                    break
            if is_booked:
                continue  # 如果已被預約，跳過此consultant

        if criteria == "price":
            if best_consultant is None or consultant['price'] < best_value:
                best_consultant = consultant
                best_value = consultant['price']
        else:
            if best_consultant is None or consultant['rate'] > best_value:
                best_consultant = consultant
                best_value = consultant['rate']

    if best_consultant is not None:
        if best_consultant['name'] not in bookings:
            bookings[best_consultant['name']] = []
        bookings[best_consultant['name']].append((hour, hour + duration))
        print(f"{best_consultant['name']}")
    else:
        print("No Service")

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]

print("=== TASK 2 ===")
book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")   # John
book(consultants, 11, 1, "rate")   # Bob
book(consultants, 11, 2, "rate")   # No Service
book(consultants, 14, 3, "price")  # John

# Task 3
def func(*data):
    # your code here
    middle_names_count = {}
    for name in data:
        if len(name) == 2:
            middle_name = name[-1]
        elif len(name) == 3 or len(name) == 4:
            middle_name = name[-2]
        elif len(name) == 5:
            middle_name = name[-3]    
        else:
            continue
        
        # 計數中間名出現的次數
        if middle_name in middle_names_count:
            middle_names_count[middle_name] += 1
        else:
            middle_names_count[middle_name] = 1

    # unique_middle_name = [name for name, count in middle_names_count.items() if count == 1]
    unique_middle_name = []
    for name, count in middle_names_count.items():
        if count == 1:
            unique_middle_name.append(name)

    if len(unique_middle_name)==0:
        print("沒有")
        return 

    # 找出具有獨一無二中間名的全名
    for name in data:
        if len(name) == 2:
            if name[-1] in unique_middle_name:
                print(name)
                return
        elif len(name) == 3 or len(name) == 4:
            if name[-2] in unique_middle_name:
                print(name)
                return
        elif len(name) == 5:
            if name[-3] in unique_middle_name:
                print(name)
                return 

print("=== TASK 3 ===")
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

# Task 4
# rule: 4 4 -1 (7)
def get_number(index):
# your code here
    root = (index//3)*7
    loop_pos = index%3
    if loop_pos==1:
        print(root+4)
    elif loop_pos==2:
        print(root+8)
    else:
        print(root)

print("=== TASK 4 ===")
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

# Task 5
def find(spaces, stat, n):
    avail_space =[]
    for x,y in zip(spaces,stat):
        avail_space.append(x * y)
    # print(avail_space) 

    best_value=max(avail_space)
    for avail_value in avail_space:
        if avail_value>=n and avail_value<best_value:
            best_value=avail_value

    if(best_value==max(avail_space)):
        print(-1)     
    else:       
        print(avail_space.index(best_value))

# your code here
print("=== TASK 5 ===")
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2
