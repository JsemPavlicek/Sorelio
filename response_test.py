# Test case = With Python and Playwright, verify the responses on the website https://www.sorelio.cz
# # after submitting an application for the Junior PHP Developer position.


from playwright.sync_api import sync_playwright

def create_locator(page,selector):
    """
   This function creates a locator for a given page and selector.
    It returns an object of type Locator that can be used to interact with the page elements.
    returns: Locator object
    """

    created_locator = page.locator(selector)
    return created_locator


def response_handle(response):
    """
    This function handles a response from the web page.
    This function appends a response.status into the responses_list = []
    returns: none
    """
    responses_list.append(response.status)




# creating of variables
responses_list = []
name = "Pavel Formánek"
email = "Jsempavlicek@seznam.cz"
textarea_text = """Dobrý den,
zaujala mě vaše nabídka na pozici junior PHP Developer a možnost připojit se k vašemu týmu. 
Rád přijímám výzvy spolu s možností naučit se něco nového, protože jedině tak má člověk možnost udělat opět krok vpřed a někam se posunout. I když musím popravdě říci, že už mi učení a posun nejde tak lehce, jako když jsem byl mladší. Začal jsem se proto učit Python a zajímat se o počítače. 
Tím jsem zjistil, že se mi líbí řešení problémů pomocí logických postupů a vím, že tyto dovednosti jsou přenositelné i do jiných programovacích jazyků, např. i do onoho PHP o které bych měl zájem:-)
Z důvodu rozšíření svých znalostí jsem tento rok absolvoval rekvalifikační kurz u společnosti ENGETO, který byl zaměřený na testování softwaru a v kterém byly základy programovacího jazyka Python, SQL, GIT a GitHubu.
Zatím jsem ještě v IT oboru nepracoval a nemám tak žádné pracovní zkušenosti. Rád bych to ale změnil a spojil svůj zájem s profesí a také se posunul opět o nějaký ten level výše.
Přikládám Vám ke své odpovědi životopis, ve kterém mám uveden odkaz na můj profil na GitHubu, kde sdílím několik repositories s automatizovanými testy na různé webové stránky. 
Za případnou zpětnou odezvu děkuji.
S pozdravem Formánek Pavel
 """

with sync_playwright() as p:
    browser = p.chromium.launch(headless= False)
    page = browser.new_page()
    page.goto('https://www.sorelio.cz/')
    page.wait_for_load_state("networkidle")
    li_a_career = create_locator(page,'a[href="https://www.sorelio.cz/career"]').nth(0)
    li_a_career.click()
    a_btn_programmer_junior = create_locator(page, '[href="https://www.sorelio.cz/career/programmer_junior"]')
    a_btn_programmer_junior.click()
    input_name = create_locator(page, 'input[name="name"]')
    input_name.type(name)
    input_email = create_locator(page,'input[name="email"]')
    input_email.type(email)
    textarea = create_locator(page, 'textarea[name="description"]')
    textarea.type(textarea_text)
    input_for_file = create_locator(page, 'input[type="file"]')
    input_for_file.set_input_files('Empty_test_CV.pdf')
    page.on('response', response_handle)
    submit = create_locator(page, 'input[type="submit"]')
    submit.click()
    page.wait_for_timeout(3000)
    page.screenshot(path='test_result_photo.png', full_page= True)
    error_div = create_locator(page,'div.contact-form-error alert alert-danger mt-4')

    page.wait_for_timeout(10000)
    browser.close()

for one_response in responses_list:
    print(f"HTTP status code is: {one_response}")

if 500 in responses_list:
    print("error")
else:
    print("test passed")
