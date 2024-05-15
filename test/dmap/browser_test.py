



#def navigate_to_student_dashboard_page(driver, student_id):
#    """requires the logged in user to have admin access to student search!"""
#    print(driver.title)
#    breakpoint()
#
#    #
#    # PART ONE (SEARCH)
#    #
#
#    #student_id_input = driver.find_element(By.NAME, "studentSearch-label")
#    #student_id_input = driver.find_element(By.ID, "studentSearch-label")
#    #student_id_input = driver.find_element(By.XPATH, '//input[@aria-label="hidden-search-input"]')
#
#    #input_element = driver.find_element(By.XPATH, '//input[@aria-label="hidden-search-input"]')
#
#    #driver.implicitly_wait(3)
#
#    input_field = driver.find_element(By.ID, 'studentSearch')
#    input_field.clear()  # Clears any pre-filled text in the input box
#    input_field.send_keys(student_id)
#    #search_button = driver.find_element(By.ID, 'studentSearch_Adornment')
#    #search_button.click()
#    # press enter to search!
#    input_field.send_keys(Keys.ENTER)
#
#
#    #search_button = driver.find_element(By.XPATH, '//button[text()="SEARCH"]')  # CHECK XPATH
#    #search_button.click()
#    print(driver.title)
#
#    #
#    # PART TWO (SELECT)
#    #
#
#    #wait_condition = EC.element_to_be_clickable((By.XPATH, '//button[text()="SELECT"]'))
#    #search_button = WebDriverWait(driver, 10).until(  wait_condition  )
#    #search_button.click()
#    #print(driver.title)
#
#    return driver.page_source
