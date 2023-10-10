
from MedWorkNew import *

def test():
    # ---
    # python3 pwb.py newupdater/MedWorkNew
    import pywikibot
    # ---
    old_params.printn = print
    mv_section.printn = print
    chembox.printn = print
    drugbox.printn = print
    expend.printn = print
    expend_new.printn = print
    # ---
    Dir = Path(__file__).parent
    # ---
    text = codecs.open(os.path.join(Dir, "bots/resources.txt"), "r", "utf-8").read()
    newtext = work_on_text("test", text)
    # ---
    pywikibot.showDiff(text, newtext)
    # ---
    codecs.open(os.path.join(Dir, "bots/resources_new.txt"), "w", "utf-8").write(newtext)

    # ---


if __name__ == "__main__":
    test()
