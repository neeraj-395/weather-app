import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from typing import Any, Optional, Dict, Tuple


def create_labels(parent: Any, key_pairs: Dict[str, str], config: Dict[str, dict]) -> Tuple[Dict[str, tk.Label], Dict[str, tk.Label]]:
    """
    Creates parameter and value labels in a specified parent widget.

    This function generates a set of labels within a parent widget, 
    based on key pairs that define the label texts and a configuration 
    dictionary for label styling. It returns dictionaries containing the 
    created parameter and value labels.

    ### Args:
    - parent (Any): The parent widget in which the labels will be created.
    - key_pairs (Dict[str, str]): A dictionary where the keys are destination 
      label texts and the values are source label texts.
    - config (Dict[str, dict]): A configuration dictionary specifying the styling 
      for each label. The keys should correspond to destination label texts or 'FOR_ALL' 
      for default styling.

    ### Returns:
    Tuple[Dict, Dict]: Two dictionaries:
    - param_label: A dictionary of created parameter labels.
    - value_label: A dictionary of created value labels.

    ### Example:
        >>> import tkinter as tk
        >>> root = tk.Tk()
        >>> key_pairs = {"Temperature": "temp", "Humidity": "hum"}
        >>> config = {"Temperature": {"bg": "lightblue"}, "FOR_ALL": {"font": ("Arial", 12)}}
        >>> param_labels, value_labels = create_labels(root, key_pairs, config)
        >>> root.mainloop()

    ### Note:
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    param_label, value_label = {}, {}

    for i, dest_key in enumerate(key_pairs.keys()):

        label_config = config.get(dest_key, config.get('FOR_ALL',{}))
        param_label[dest_key] = tk.Label(parent, text=f"{dest_key}:", **label_config)
        param_label[dest_key].grid(row=i, column=0, padx=1, pady=1, sticky="w")

        value_label[dest_key] = tk.Label(parent, text="N/A", **label_config)
        value_label[dest_key].grid(row=i, column=1, padx=1, pady=1, sticky="w")

    return param_label, value_label


def create_card(file: Any, size: Optional[Tuple[int,int]] = None, corner_radius: Optional[int] = None):
    """
    Creates a card image with optional resizing and rounded corners.

    This function opens an image file and optionally resizes it and applies rounded corners. 
    The result is returned as an `ImageTk.PhotoImage` object, suitable for use in Tkinter applications.

    ### Args:
    - file (Any): The file path or file-like object containing the image.
    - size (Optional[Tuple[int, int]]): An optional tuple specifying the desired size (width, height) to resize the image. If None, the image is not resized.
    - corner_radius (Optional[int]): An optional integer specifying the radius of the rounded corners. If None, the image corners are not rounded.

    ### Example:
        >>> from PIL import ImageTk
        >>> import tkinter as tk
        >>> from your_module import create_card

        >>> root = tk.Tk()
        >>> file_path = "path/to/your/image.png"
        >>> card_image = create_card(file_path, size=(300, 200), corner_radius=20)
        >>> label = tk.Label(root, image=card_image)
        >>> label.pack()
        >>> root.mainloop()

    ### Note:
    This function documentation was generated with the assistance of ChatGPT, 
    an AI language model developed by OpenAI.
    """

    # Open the image file
    img = Image.open(file)

    # Resize the image if necessary
    if size is not None and img.size != size: img = img.resize(size, Image.LANCZOS) # type: ignore
    if corner_radius is None: return ImageTk.PhotoImage(img)

    # Create a mask with rounded corners
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), corner_radius, fill=255)

    # Apply the mask to the image
    result = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    result.paste(img.convert("RGBA"), (0, 0), mask=mask)

    return ImageTk.PhotoImage(result)