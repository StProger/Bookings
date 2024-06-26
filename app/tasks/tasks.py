from app.tasks.celery import celery

from PIL import Image

from pathlib import Path


@celery.task(name='')
def process_pic(
        path: str
):

    im_path = Path(path)
    im = Image.open(path)

    res_im_1000_500 = im.resize((1000, 500))
    res_im_200_100 = im.resize((200, 100))

    res_im_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    res_im_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")
