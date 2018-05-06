

SOCIAL_TYPES=(
    ('fb','facebook'),
    ("tw","twitter"),
    ("ig","instagram"),
    ("pn","pintrest"),

)


def blogImagePath(instance, filename):
    return "media/{authorId}/{id}/{file}".format(id=instance.id, authorId=instance.author.id, file=filename)

def profileImagePath(instance, filename):
    return "media/{profileId}/profile/{file}".format(profileId=instance.id, file=filename)


def generate_username(first_name, last_name):
        from blog.models import Profile
        name = "{0}{1}".format(first_name[0], last_name).lower()
        index = 0
        while True:
            if index == 0 and Profile.objects.filter(handle=name).count() == 0:
                return name
            else:
                new_val = "{0}{1}".format(name, index)
                if Profile.objects.filter(handle=new_val).count() == 0:
                    return new_val
            index += 1
            if index > 10000:
                raise Exception("Name is too common!")

# def extractTags(data):
#     tags = json.loads(data["tags"])
#     TagSerializer(data=tags, many=True).is_valid(raise_exception=True)
#     data.pop("tags")
#     return tags
