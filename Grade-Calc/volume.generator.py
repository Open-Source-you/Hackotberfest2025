# Function to calculate the volume of a rectangular prism
def calculate_volume(length, width, height):
    return length * width * height


# Get user input for dimensions
length = float(input("Enter the length of the rectangular prism: "))
width = float(input("Enter the width of the rectangular prism: "))
height = float(input("Enter the height of the rectangular prism: "))

# Calculate the volume
volume = calculate_volume(length, width, height)

# Display the result
print(f"The volume of the rectangular prism is: {volume} cubic units")
