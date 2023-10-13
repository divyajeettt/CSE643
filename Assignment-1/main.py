import json
import os


def is_weather_match(preference, weather):
    return preference.casefold() == weather.casefold()


def is_budget_match(preference, cost):
    return preference >= cost


def get_common_activities(preference, activities):
    return set(preference).intersection(set(activities))


def has_common_activities(preference, activities):
    return len(get_common_activities(preference, activities)) > 0


def get_common_connectivity(preference, connectivity):
    return set(preference).intersection(set(connectivity))


def has_common_connectivity(preference, connectivity):
    return len(get_common_connectivity(preference, connectivity)) > 0


def get_average_rating(ratings):
    return sum(ratings) / len(ratings)


def is_rating_match(preference, ratings):
    return len(ratings) > 0 and preference <= get_average_rating(ratings)


def add_new_destination():
    print()

    name = input("Enter the name of the destination: ")
    if DATABASE.get(name) is not None:
        print("Destination already exists")
        return

    weather = input("Enter the type of weather: ")
    budget = int(input("Enter budget requirements: "))

    print()
    activities = []
    while True:
        activities.append(input("Enter a popular activity in the destination: "))
        choice = input("Do you want to add more activities? [Y/N]: ").casefold()
        if choice == "n":
            break

    print()
    connectivity = []
    while True:
        connectivity.append(input("Enter a mode of connectivity to the destination: "))
        choice = input("Do you want to add more modes of connectivity? [Y/N]: ").casefold()
        if choice == "n":
            break

    row = {
        "weather": weather,
        "budget": budget,
        "activities": activities,
        "connectivity": connectivity,
        "rating": [],
        "feedback": []
    }

    feedback = input("Do you want to add feedback? [Y/N]: ").casefold()
    if feedback == "y":
        add_feedback(row=row)

    DATABASE[name] = row
    print("Destination added successfully")


def recommend_destination():
    print()
    if not DATABASE:
        print("There are no destinations in the database!")
        print("Please add a destination first.")
        return

    print("Let us take a look at your preferences")
    weather = input("Enter the type of weather: ")
    budget = int(input("Enter your budget: "))

    print()
    activities = []
    while True:
        activities.append(input("Enter a tourist activity you prefer: "))
        choice = input("Do you want to enter more activities? [Y/N]: ").casefold()
        if choice == "n":
            break

    print()
    connectivity = []
    while True:
        connectivity.append(input("Enter a mode of connectivity you prefer: "))
        choice = input("Do you want to enter more modes of connectivity? [Y/N]: ").casefold()
        if choice == "n":
            break

    rating = float(input("Enter the minimum average rating you prefer: "))
    print()

    recommendations = []
    for name, row in DATABASE.items():
        matches = name, []
        match_tracker = {
            "weather": False, "budget": False,
            "activities": False, "connectivity": False, "rating": False
        }

        if is_weather_match(weather, row["weather"]):
            matches[1].append("weather")
            match_tracker["weather"] = True

        if is_budget_match(budget, row["budget"]):
            matches[1].append("budget")
            match_tracker["budget"] = True

        if has_common_activities(activities, row["activities"]):
            matches[1].append(f"activities - {get_common_activities(activities, row['activities'])}")
            match_tracker["activities"] = True

        if has_common_connectivity(connectivity, row["connectivity"]):
            matches[1].append(f"connectivity - {get_common_connectivity(connectivity, row['connectivity'])}")
            match_tracker["connectivity"] = True

        if is_rating_match(rating, row["rating"]):
            matches[1].append(f"rating - {get_average_rating(row['rating'])}")
            match_tracker["rating"] = True

        is_match = match_tracker["weather"] or match_tracker["budget"] or match_tracker["activities"] or \
                   match_tracker["connectivity"] or match_tracker["rating"]
        if is_match:
            recommendations.append(matches)

    if not recommendations:
        print("No destinations found")
    else:
        print("The following destinations match your preferences:")
        for i, (name, reason) in enumerate(recommendations, start=1):
            print(f"MATCH #{i}: {name}")
            print("matches your preferred", reason)
            choice = input("Do you want to view feedback for this destination? [Y/N]: ").casefold()
            if choice == "y":
                print("Feedback:")
                for feedback in DATABASE[name]["feedback"]:
                    print(feedback)
            print()


def add_feedback(row=None, fetch=False):
    if not DATABASE:
        print("There are no destinations in the database!")
        print("Please add a destination first.")
        return

    if fetch:
        name = input("Enter the name of the destination to add feedback for: ")
        if DATABASE.get(name) is None:
            print("Destination not found")
            return
    else:
        name = row["name"]

    rating = float(input(f"Enter the rating for {name}: "))
    feedback = input(f"Enter the feedback for {name}: ")
    DATABASE[name]["rating"].append(rating)
    DATABASE[name]["feedback"].append(feedback)
    print("Feedback added successfully")


def main():
    while True:
        print("Welcome to the Travel Recommendation System")
        print("1. Add a new destination")
        print("2. Recommend a destination")
        print("3. Add feedback for a destination")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_new_destination()
        elif choice == "2":
            recommend_destination()
        elif choice == "3":
            add_feedback(fetch=True)
        elif choice == "4":
            print("Thank you for using the Travel Recommendation System")
            break
        else:
            print("Invalid choice")

        input("Press enter to continue...")
        print()


if __name__ == "__main__":
    if not os.path.exists("database.json"):
        with open("database.json", "w") as f:
            json.dump({}, f, indent=4)

    with open("database.json", "r") as f:
        DATABASE = json.load(f)

    main()
    with open("database.json", "w") as f:
        json.dump(DATABASE, f, indent=4)