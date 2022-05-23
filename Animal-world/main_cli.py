from Model.Area import create_area_from_database

area = None
while area is None:
    path = input("Input name of the file:\n")
    print("Initial area:")
    area = create_area_from_database(path)

area.display_area()
area.menu()
