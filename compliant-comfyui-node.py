import gradio_client, requests, random
CL = gradio_client.Client("KBlueLeaf/DTG-demo")
from pathlib import Path
if Path(".artists.txt").exists() == False:
    Path(".artists.txt").write_text(requests.get("https://github.com/KohakuBlueleaf/z-a1111-sd-webui-dtg/raw/main/tag-list/meta.txt").text)
if Path(".characters.txt").exists() == False:
    Path(".characters.txt").write_text(requests.get("https://github.com/KohakuBlueleaf/z-a1111-sd-webui-dtg/raw/main/tag-list/char.txt").text)
if Path(".copyrights.txt").exists() == False:
    Path(".copyrights.txt").write_text(requests.get("https://github.com/KohakuBlueleaf/z-a1111-sd-webui-dtg/raw/main/tag-list/copyright.txt").text)
ARTISTS = Path(".artists.txt").read_text().split("\n")
CHARS = Path(".characters.txt").read_text().split("\n")
COPYR = Path(".copyrights.txt").read_text().split("\n")
class DanTagGen:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "blacklist": ("STRING", {"multiline": True}),
                "length": (["very_short", "short", "long", "very_long"], {"default": "long"}),
                "width": ("INT", {
                    "min": 64,
                    "max": 2048,
                    "default": 1024
                }),
                "height": ("INT", {
                    "min": 64,
                    "max": 2048,
                    "default": 1024
                }),
                "temp": ("FLOAT", {
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "default": 0.75
                }),
                "escape_bracket": (["enable", "disable"], {"default": "enable"}),
                "model": (["alpha", "beta"], {"default": "beta"}),
                "rating": (["safe", "sensitive", "nsfw", "nsfw, explicit"], {"default": "safe"}),
                "regenerate": (["enable", "disable", "plap"], {"default": "enable"}),
                "shuffle": (["enable", "disable"], {"default": "enable"})
            }
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "predict"

    CATEGORY = "DTG"
    def predict(self, prompt, blacklist, length, width, height, temp, escape_bracket, model, rating, regenerate, shuffle):
        artists, characters, general, copyrights = "", "", "", ""
        if "," in prompt:
            prmpt = prompt.replace(", ", ",")
            prmpt = prmpt.replace(" ", "_")
            prmpt = prmpt.replace(",", " ")
        else:
            prmpt = prompt.replace("-", "_")
        for tag in prmpt.split(" "):
            if tag in ARTISTS:
                artists += tag + " "
            elif tag in CHARS:
                characters += tag + " "
            elif tag in COPYR:
                copyrights += tag + " "
            else:
                general += tag + " "
        specials = []
        for tag in general.split(" "):
            if tag in ['1girl', '2girls', '3girls', '4girls', '5girls', '6+girls', 'multiple_girls', '1boy', '2boys', '3boys', '4boys', '5boys', '6+boys', 'multiple_boys', 'male_focus', '1other', '2others', '3others', '4others', '5others', '6+others', 'multiple_others']:
                specials.append(tag)
        if shuffle == "enable":
            random.shuffle(specials)
            lartists = artists.split(" ")
            random.shuffle(lartists)
            artists = " ".join(lartists)
            lcharacters = characters.split(" ")
            random.shuffle(lcharacters)
            characters = " ".join(lcharacters)
            lgeneral = general.split(" ")
            random.shuffle(lgeneral)
            general = " ".join(lgeneral)
            lcopyrights = copyrights.split(" ")
            random.shuffle(lcopyrights)
            copyrights = " ".join(lcopyrights)
        result = CL.predict(
            "KBlueLeaf/DanTagGen-" + model,
            rating,
            artists,
            characters,
            copyrights,
            length,
            specials,
            prmpt,
            width,
            height,
            blacklist,
            escape_bracket,	
            temp,
            api_name="/wrapper"
        )[0]
        result = result.replace("\n", " ")
        result = result.replace("  ", " ")
        return (result,)
    
    @classmethod
    def IS_CHANGED(self, prompt, blacklist, length, width, height, temp, escape_bracket, model, rating, regenerate, shuffle):
        if regenerate == "plap":
            return random.randint(1, 200) * regenerate # lol
        return random.randint(1, 2675376) * bool(regenerate) 

# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DTG": DanTagGen
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DTG": "Danbooru Tag Generator (HF Space)"
}
