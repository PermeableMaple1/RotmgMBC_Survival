import data.objects


def post_time(total_time, screen):

    total_time = round(total_time, 2)

    text = data.objects.create_text(str(total_time) + 's', 2, 25, (255, 255, 255))

    screen.blit(text, (5, 5))
