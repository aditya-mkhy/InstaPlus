import random

nature = [
    "The serenity of nature is unmatched",
    "Nature has a way of putting everything into perspective",
    "The beauty of the outdoors is truly awe-inspiring",
    "Lost in the vastness of nature's wonders",
    "Breathing in the fresh airr isss invigorating",
    "Nature's tranquility is the ultimate escape",
    "Finding solace in the midst of nature's embrace.",
    "Every corner of the earth holds its own magic",
    "The great outdoors never ceases to amaze",
    "Chasing adventures in the heart of nature",
    "The simplicity of nature is its greatest charm",
    "In the presence of towering peaks, we find humility.",
    "Nature's beauty is a reminder of life's wonders.",
    "Captivated by the natural world's boundless beauty.",
    "Exploring the wilderness fuels the spirit of adventure.",
    "Finding peace in the rhythm of nature's heartbeat.",
    "Nature's palette paints the most magnificent landscapes."

    "Absolutely stunning!",
    "Incredible capture!",
    "Wow, this is breathtaking!",
    "Beautiful scenery!",
    "Absolutely gorgeous!",
    "What a magnificent view!",
    "This is amazing!",
    "So picturesque!",
    "Absolutely fantastic!",
    "This is truly mesmerizing!",
    "Speechless",
    "So peaceful and serene!",
    "Absolutely lovely!",
    "This is just perfect!",
    "What a sight to behold!",
    "Absolutely splendid!",
    "So tranquil and beautiful!",
    "Simply stunning!",
    "This is pure beauty!",
    "This is magical!",

    "Wowowo", 
    "wowz",
    "Beautiful shot", 
    "Unbelievable", 
    "Wow that make me Speechless", 
    "Magnifique", 
    "Out of this world!",
    "woww Aammmazzing"
]

class TextComments:
    def __init__(self) -> None:
        self.comments_list = nature.copy()

    @property
    def get_comment(self):
        cmnt = random.choice(self.comments_list)
        self.comments_list.remove(cmnt)

        if len(self.comments_list) < 1:
            self.comments_list = nature.copy()
        print("len==>", len(self.comments_list))
        return cmnt
    
if __name__ == "__main__":
    text_cmnt = TextComments()
    print(text_cmnt.comment)
