from tkinter import *
from tkinter import ttk




def loadRecipes():

    """
    Reads image paths from 'imagePath.txt' and production recipes from 'recipes.txt'
    to create and return data dictionary using item names as keys.
    """
    

    #--- Loading Image Paths ---
    image_paths = {}
    
    # Read the image file (Expected format: Item_Name = Image_Path)
    try:
        with open("imagePath.txt", "r", encoding="utf-8") as img_file:
            for line in img_file:
                if not line.strip() or "=" not in line:
                    continue
                
                parts = line.split("=")
                item_name = parts[0].strip()
                img_path = parts[1].strip()  
                
                image_paths[item_name] = img_path

    # Print a warning to the terminal instead of crashing if the file is missing
    except FileNotFoundError:
        print("Warning: 'imagePath.txt' not found. Images will not be loaded.")
    

    #--- Loading Production Recipes ---

    recipes = {}
    with open("recipes.txt", "r", encoding="utf-8") as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue
                
            # Split the line by commas and remove extra spaces
            data = [info.strip() for info in line.split(',')]
            
            # Core details (First 3 columns are always fixed)
            item_name = data[0]
            machine = data[1]
            production_rate = int(data[2])

            # Create an empty dictionary for the ingredients
            ingredients = {}
            
            # Start from the 4th index and jump by 2 to get (Ingredient, Amount) pairs
            for i in range(3, len(data), 2):
                ingredient_name = data[i]
                ingredient_amount = int(data[i+1])
                ingredients[ingredient_name] = ingredient_amount
                
            # Create the recipe dictionary and append it to the main list
            recipes[item_name] = {
                "machine": machine,
                "production_rate_per_min": production_rate,
                "ingredients": ingredients,
                # Fetch the image path using the item name
                # (Defaults to 'None' if the image is not found in the first stage)
                "image_path": image_paths.get(item_name, None)
            }
            
           
    return recipes
data = loadRecipes()

def calculation(name):
    """
    Calculates the required amount of ingredients based on the desired production 
    amount and dynamically displays the results (text and images) in the GUI.
    """
    
        
    boxes =[]
    def addToBox():
        
            
        # Get the desired production amount from the user input (Entry widget)
        desiredAmount = int(ENTRY_Amount.get())


        # # --- 1. CLEANUP PHASE ---
        # # Destroy all existing widgets in the frame to prevent overlapping
        # for widget in frame_Calc.winfo_children():
        #     widget.destroy()
        # boxes.clear()

        #--- SETUP PHASE ---
        current_col = len(frame_Calc.winfo_children())
        new_box = Frame(frame_Calc, bd=2, relief="groove", padx=10, pady=10)
        new_box.pack(side="left", padx=10, anchor="n")
 
        BTTN_Remove = Button(new_box,width=15,text="Remove", command=lambda:new_box.destroy())
        BTTN_Remove.grid(row=0, column=1, padx=10, sticky="w")
         
        # Fetch the selected item's recipe data from the main dictionary
        ingr = data.get(name, {})
        gridRow = 0
        gridCol = 0


        # --- 2. MATH & CALCULATIONS PHASE ---
        item_list = [name]             # Will store the names of items to display
        ratios = []                    # Base ingredient amounts from the recipe
        realRatios = []                # Calculated ingredient amounts based on desired output

        productionRate = ingr.get("production_rate_per_min")

        # Safely fetch ingredients (using default {} to avoid crashes on raw materials)
        ingredients_dict = ingr.get('ingredients', {})

        # Extract base amounts for each ingredient
        for i in ingredients_dict.values():
            ratios.append(i)

        # Extract names for each ingredient
        for item in ingredients_dict.keys():
            item_list.append(item)

        # The first item in realRatios is the desired amount of the main product itself
        realRatios.append(desiredAmount)

        # Calculate the required amount for each ingredient using direct proportion:
        # Required = (Base Ingredient Amount * Desired Output Amount) / Base Production Rate
        for i in ratios:
            realRatios.append((i * desiredAmount) / productionRate )
        
        
        # --- 3. GUI RENDERING PHASE ---    
        count = 0

        # Loop through the combined list of items (main product + its ingredients)
        for item in item_list:
            # Get the specific product's data to fetch its image path
            product = data.get(item, {})
            
            # Create and place the label for the item's name
            newLabel = Label(new_box, text=item)
            newLabel.grid(row=gridRow, column=gridCol)

            # Create the label for the calculated required amount
            # (Using :.2f to format numbers like 33.3333 to 33.33 for a cleaner UI)
            amount_text = f"{realRatios[count]:.2f}"
            newLabel2 = Label(new_box, text=amount_text)
            count += 1

            # Fetch and process the image
            img_path = product.get("image_path")
        
            if img_path: 
                try:
                    ingrImage = PhotoImage(file=img_path)
                    resized_image = ingrImage.subsample(3, 3)
                    L_ingrImage = Label(new_box, image=resized_image)
                    L_ingrImage.image = resized_image 
                except Exception:
                    
                    L_ingrImage = Label(new_box, text="(Resim Hatası)")
            else:
               
                L_ingrImage = Label(new_box, text="(No Image)")

            # Move to the next row to place the image and the amount label side-by-side
            gridRow += 1
            L_ingrImage.grid(row=gridRow, column=gridCol)
            newLabel2.grid(row=gridRow, column=gridCol+1, padx=10, sticky="w")

            gridRow += 1
         
            # Move down one more row for the next item in the loop
            gridRow += 1

            
    addToBox()    

root = Tk()
root.title("Satisfactory Calculator")
root.geometry("500x500")






filterOptions = set()
filterOptions.add("All")
for i in data.keys():
    product = data.get(i)
    machine = product.get("machine")
    filterOptions.add(machine)

def filterProducts(selected):
    list1= []
    for i in data.keys():
        product = data.get(i)
        if product.get("machine") == selected:
            list1.append(i)
    return list1



def loadButton():
    combobox_RecipeNames["values"] =()
    combobox_filter["values"] = list(filterOptions)
    combobox_RecipeNames["values"] = list(data.keys())
    combobox_RecipeNames.set('')


def calculateButton():
    selected = combobox_RecipeNames.get()
    calculation(selected)

def FilterSearch():
    selected = combobox_filter.get()
    combobox_RecipeNames["values"] =()
    combobox_RecipeNames.set('')
    if (selected == "All" or selected == ""):
        combobox_RecipeNames["values"] = list(data.keys())
    else:
        list1 = filterProducts(selected)
        combobox_RecipeNames["values"] = list1
        
  




frame_head = Frame(root, bd=2, relief="groove")   
frame_Calc = Frame(root, bd=2, relief="groove")            

frame_head.grid(column=0, row=0 , pady=10, padx=10, sticky="nsew")
frame_Calc.grid(column=0, row=1 , pady=10, padx=10, sticky="nsew")

combobox_RecipeNames = ttk.Combobox(frame_head)
combobox_filter = ttk.Combobox(frame_head)


BTTN_Load = Button(frame_head,width=15,text="Load Recipes", command=lambda:loadButton())
BTTN_Calculate = Button(frame_head,width=15,text="Calculate", command=lambda:calculateButton())
BTTN_FilterSearch = Button(frame_head,width=15,text="Filter Search", command=lambda:FilterSearch())

productImage = PhotoImage()
ENTRY_Amount = Entry(frame_head,  width=7)
ENTRY_Amount.insert(0,"0")

    

combobox_RecipeNames.grid(column=0, row=0) 
combobox_filter.grid(column=1, row=0) 



BTTN_Calculate.grid(column=0, row=1)
BTTN_Load.grid(column=2, row=0)
BTTN_FilterSearch.grid(column=2, row=1)
ENTRY_Amount.grid(column=1, row=1)

root.mainloop()

