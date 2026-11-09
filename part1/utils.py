import cv2
import matplotlib.pyplot as plt

# ==================================
# Show Original and Preview
# ==================================

def show_image(original, preview, title):
    plt.figure(figsize=(10, 5))

    # Original image
    plt.subplot(1, 2, 1)
    if len(original.shape) == 2:
        plt.imshow(original, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis("off")

    # Preview image
    plt.subplot(1, 2, 2)
    if len(preview.shape) == 2:
        plt.imshow(preview, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# ==================================
# History Display
# ==================================

def show_history(history):
    print("\n========== History ==========")
    if len(history) == 0:
        print("No operations performed yet")
    else:
        for i, item in enumerate(history, 1):
            print(str(i) + ". " + item)
    print("=============================\n")

# ==================================
# Save Image
# ==================================

def save(img, filename):
    cv2.imwrite(filename, img)
    print("Image saved successfully!")