from PIL import Image

image_number = 31

for image in range(image_number):
    path = f"./uploads/room_photos/{image + 1}.webp"
    im = Image.open(path)
    im.save(f"./uploads/room_photos/{image + 1}.webp", "jpeg")