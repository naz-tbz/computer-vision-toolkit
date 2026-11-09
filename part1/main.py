import cv2

from operations import brightness
from operations import contrast
from operations import grayscale
from operations import padding
from operations import threshold
from operations import blend

from utils import show_image
from utils import show_history
from utils import save


# ==================================
# Load Image
# ==================================

path = input("Enter image path (example: images/photo.jpg): ")
image = cv2.imread(path)
if image is None:
    print("Cannot load image")
    exit()
original = image.copy()
current = image.copy()

undo = []      # Undo stack
history = []   # History log

# ==================================
# Menu
# ==================================

while True:
    print("""
========== Mini Photo Editor ==========

1. Adjust Brightness
2. Adjust Contrast
3. Convert to Grayscale
4. Add Padding
5. Apply Thresholding
6. Blend With Another Image
7. Undo Last Operation
8. View History
9. Save and Exit

=======================================
""")
    choice = input("Choose option (1-9): ")

    # ==================================
    # Brightness
    # ==================================
    if choice == "1":
        try:
            value = int(input("Brightness (-255 to 255, example: 50): "))
        except ValueError:
            print("Invalid number, try again.")
            continue

        undo.append(current.copy())
        current = brightness(current, value)
        history.append("Brightness " + str(value))
        show_image(original, current, "Brightness")

    # ==================================
    # Contrast
    # ==================================
    elif choice == "2":
        try:
            value = float(input("Contrast (example: 1.5 more, 0.5 less): "))
        except ValueError:
            print("Invalid number, try again.")
            continue

        undo.append(current.copy())
        current = contrast(current, value)
        history.append("Contrast " + str(value))
        show_image(original, current, "Contrast")

    # ==================================
    # Grayscale
    # ==================================
    elif choice == "3":
        undo.append(current.copy())
        current = grayscale(current)
        history.append("Converted to grayscale")
        show_image(original, current, "Grayscale")

    # ==================================
    # Padding
    # ==================================
    elif choice == "4":
        try:
            size = int(input("Extra padding size (example: 20 pixels): "))
        except ValueError:
            print("Invalid number, try again.")
            continue

        print("""
Border Type:

1. Constant
2. Reflect
3. Replicate
""")
        border_choice = input("Choose border type: ")
        if border_choice == "1":
            border = "constant"
        elif border_choice == "2":
            border = "reflect"
        elif border_choice == "3":
            border = "replicate"
        else:
            print("Invalid choice, defaulting to replicate.")
            border = "replicate"

        print("""
Padding Ratio:

1. Square (1:1)
2. Rectangle (example 4:3)
3. Custom Ratio (example 4:5)
""")
        ratio_choice = input("Choose ratio: ")
        try:
            if ratio_choice == "1":
                ratio_w = 1
                ratio_h = 1
                ratio_name = "Square"
            elif ratio_choice == "2":
                ratio_w = float(input("Enter width ratio (example 4): "))
                ratio_h = float(input("Enter height ratio (example 3): "))
                ratio_name = "Rectangle " + str(ratio_w) + ":" + str(ratio_h)
            else:
                ratio = input("Enter custom ratio W:H (example 4:5): ")
                parts = ratio.split(":")
                ratio_w = float(parts[0])
                ratio_h = float(parts[1])
                ratio_name = ratio
        except (ValueError, IndexError):
            print("Invalid ratio, try again.")
            continue

        undo.append(current.copy())
        current = padding(current, size, border, ratio_w, ratio_h)
        history.append("Padding " + str(size) + "px " + border + " " + ratio_name)
        show_image(original, current, "Padding")

    # ==================================
    # Threshold
    # ==================================
    elif choice == "5":
        print("""
Threshold Type:

1. Binary
2. Binary Inverse
""")
        try:
            t = int(input("Choose type (1 or 2): "))
            value = int(input("Threshold value (0-255, example: 127): "))
        except ValueError:
            print("Invalid number, try again.")
            continue

        undo.append(current.copy())
        current = threshold(current, t, value)
        history.append("Threshold value " + str(value))
        show_image(original, current, "Threshold")

    # ==================================
    # Blend
    # ==================================
    elif choice == "6":
        path2 = input("Second image path: ")
        img2 = cv2.imread(path2)
        if img2 is None:
            print("Cannot load second image")
            continue

        try:
            alpha = float(input("Alpha (0-1, example 0.5): "))
        except ValueError:
            print("Invalid number, try again.")
            continue

        undo.append(current.copy())
        current = blend(current, img2, alpha)
        history.append("Blend alpha " + str(alpha))
        show_image(original, current, "Blend")

    # ==================================
    # Undo
    # ==================================
    elif choice == "7":
        if len(undo) > 0:
            current = undo.pop()
            history.append("Undo")
            show_image(original, current, "Undo")
        else:
            print("Nothing to undo")

    # ==================================
    # History
    # ==================================
    elif choice == "8":
        show_history(history)

    # ==================================
    # Save and Exit
    # ==================================
    elif choice == "9":
        show_history(history)
        answer = input("Save final image? (y/n): ")
        if answer.lower() == "y":
            filename = input("Filename (example result.jpg): ")
            save(current, filename)
        print("Goodbye!")
        break

    else:
        print("Invalid option")