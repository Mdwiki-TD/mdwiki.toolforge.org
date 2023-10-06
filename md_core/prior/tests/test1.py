from prior import p4
from prior import read4

# ---
lal = [
    "Esophageal cancer",
    "Pancreatic cancer",
    "Brain tumor",
    "Cancer",
    "Leukemia",
    "Lymphoma",
    "Cervical cancer",
    "Colorectal cancer",
    "Breast cancer",
    "Skin cancer",
    "Prostate cancer",
    "Stomach cancer",
    "Ovarian cancer",
    "Endometrial cancer",
    "Melanoma",
    "Glioblastoma",
    "Lung cancer",
    "Mesothelioma",
    "Multiple myeloma",
    "Hodgkin lymphoma",
    "Non-Hodgkin lymphoma",
    "Head and neck cancer",
    "Liver cancer",
    "Myelodysplastic syndrome",
    "Neurofibromatosis",
    "Neuroblastoma",
    "Basal-cell carcinoma",
    "Cutaneous squamous-cell carcinoma",
    "Bladder cancer",
    "Thyroid cancer",
    "Meningioma",
    "Benign prostatic hyperplasia",
    "Lipoma",
    "Kaposi's sarcoma",
    "Testicular cancer",
    "Acute myeloid leukemia",
    "Chronic lymphocytic leukemia",
    "Acute lymphoblastic leukemia",
    "Teratoma",
    "Cholangiocarcinoma",
    "Uterine cancer",
    "Ewing sarcoma",
    "Anal cancer",
    "Vulvar cancer",
    "Kidney cancer",
]
# ---

all, allen = p4.start_test(links=lal)

read4.work_test(all, allen)

# ---
x = 'https://books.google.ca/books?id=JaOoXdSlT9sC&pg=PA11'
# ---
# prased = url_parser(x)
# print(prased)
# ---
#
# if 'books.google' in x: x = re.sub(r'google\.\w+/', 'google.com/', x)
# ---
