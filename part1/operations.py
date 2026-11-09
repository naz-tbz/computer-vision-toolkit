import cv2

# ==============================
# Brightness
# ==============================

def brightness(img, value):
    result = cv2.convertScaleAbs(img, alpha=1, beta=value)
    return result

# ==============================
# Contrast
# ==============================

def contrast(img, value):
    result = cv2.convertScaleAbs(img, alpha=value, beta=0)
    return result

# ==============================
# Grayscale
# ==============================

def grayscale(img):
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==================================
# Padding Functions
# ==================================

def calculate_min_padding(width, height, ratio_w, ratio_h):
    """
    Calculate the smallest padding needed
    to make the image follow the selected ratio.
    """
    current_ratio = width / height
    target_ratio = ratio_w / ratio_h

    top = 0
    bottom = 0
    left = 0
    right = 0

    # Image is too wide -> add height
    if current_ratio > target_ratio:
        new_height = int(width * ratio_h / ratio_w)
        total_padding = new_height - height
        top = total_padding // 2
        bottom = total_padding - top

    # Image is too tall -> add width
    elif current_ratio < target_ratio:
        new_width = int(height * ratio_w / ratio_h)
        total_padding = new_width - width
        left = total_padding // 2
        right = total_padding - left

    return top, bottom, left, right


def add_extra_ratio_padding(top, bottom, left, right, extra_size, ratio_w, ratio_h):
    """
    Add the user's extra padding size while keeping the selected ratio.
    """
    if extra_size <= 0:
        return top, bottom, left, right

    # Divide extra padding according to ratio so the aspect ratio is preserved
    extra_width = int(extra_size * ratio_w / (ratio_w + ratio_h))
    extra_height = extra_size - extra_width

    left += extra_width // 2
    right += extra_width - (extra_width // 2)

    top += extra_height // 2
    bottom += extra_height - (extra_height // 2)

    return top, bottom, left, right


def padding(img, extra_size, border, ratio_w, ratio_h):
    height, width = img.shape[:2]

    # Step 1: minimum padding to reach the target ratio
    top, bottom, left, right = calculate_min_padding(width, height, ratio_w, ratio_h)

    # Step 2: add the user's requested extra padding, keeping the ratio
    top, bottom, left, right = add_extra_ratio_padding(
        top, bottom, left, right, extra_size, ratio_w, ratio_h
    )

    if border == "constant":
        border_type = cv2.BORDER_CONSTANT
    elif border == "reflect":
        border_type = cv2.BORDER_REFLECT
    elif border == "replicate":
        border_type = cv2.BORDER_REPLICATE
    else:
        # Fallback if something unexpected slipped through
        border_type = cv2.BORDER_REPLICATE

    result = cv2.copyMakeBorder(
        img, top, bottom, left, right, border_type, value=[0, 0, 0]
    )
    return result

# ==============================
# Threshold
# ==============================

def threshold(img, choice, value):
    if len(img.shape) == 2:
        gray = img
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mode = cv2.THRESH_BINARY if choice == 1 else cv2.THRESH_BINARY_INV
    _, result = cv2.threshold(gray, value, 255, mode)
    return result

# ==============================
# Blend
# ==============================

def blend(img1, img2, alpha):
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Match channels between the two images
    if len(img1.shape) == 2 and len(img2.shape) == 3:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    elif len(img1.shape) == 3 and len(img2.shape) == 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    result = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)
    return result