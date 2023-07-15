import time
from math import dist
from whereami import predict


COORDINATES = {
    "bedroom": (0, 0), "point_1": (1, 2), "point_2": (2, 4), "point_3": (3, 6), "kitchen": (4, 8)
}


def get_most_likely_location():
    curr_location = predict()
    return curr_location


def start_tracking(destination_location, starting_location):

    dest_coordinates = COORDINATES.get(destination_location)
    curr_coordinates = COORDINATES.get(starting_location)
    total_distance_to_go = dist(dest_coordinates, curr_coordinates)

    covered_dist = 0
    prev_location = starting_location
    print(f"Starting from: {prev_location}")
    if starting_location != destination_location:
        while True:
            text_1 = 'Detecting location........'
            print(text_1)
            time.sleep(10)
            current_location = get_most_likely_location()
            if current_location == destination_location:
                text_2 = 'You reached your destination'
                print(text_2)
                break
            if current_location != prev_location:
                prev_location = current_location
                current_location_coordinates = COORDINATES.get(current_location)
                covered_dist = dist(curr_coordinates, current_location_coordinates)
                text_3 = f'Current_location changed to {current_location}\nYou covered {covered_dist} units. Still {abs(total_distance_to_go - covered_dist)} units to go'
                print(text_3)
    else:
        text_4 = 'You already reached destination'
        print(text_4)


def main():
    destination_location = input('Whrere do you wanna go? ')
    starting_location = get_most_likely_location()
    start_tracking(destination_location, starting_location)


if __name__ == '__main__':
    main()