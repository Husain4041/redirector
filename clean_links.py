import json
import re

def contains_special_char(s):
    for char in s:
        if not char.isalnum():
            return True, char
    return False, ' '

def clean_models(make, model_dict):
    removed_models = []
    new_model_dict = {}
    for model in model_dict:
        # make_from_model = model.split(" ")
        make_from_model = re.findall(r"[\w']+", model)
        # print(f"This is the list of words in {model}: {make_from_model}")
        if (len(make.split(" ")) == 2 and len(make_from_model) >= 2):
            if (make.split(" ")[0] + make.split(" ")[1] == make_from_model[0].lower() or 
                make == make_from_model[0].lower() + " " + make_from_model[1].lower()):
                new_model_dict[model] = model_dict[model]
            else:
                removed_models.append(model)
        elif len(make.split(" ")) == 1:
            if (make == make_from_model[0].lower()):
                new_model_dict[model] = model_dict[model]
            else:
                removed_models.append(model)

    return new_model_dict, removed_models

if __name__ == "__main__":
    # print(clean_make("bac"))
    with open('car_data/make_model_links.json', 'r') as f:
        full_data = json.load(f)

    true_model = False
    
    for make in full_data["dubizzle"]:
        model_dict = full_data["dubizzle"][make]
        # ----- Printing the current make and models for that make ----- #
        # print(f"This is the make: {make} and these are the {len(model_dict)} current models: ")
        # for model in model_dict:
        #     print(model)
        
        new_model_dict, removed_models_list = clean_models(make, model_dict)

        print(f"These models have been removed for infringement reasons: {removed_models_list}")
        # print(f"These are the {len(new_model_dict)} true models for {make}:")
        for models in new_model_dict:
            # print(models)
            new_model_dict[models] = model_dict[models]
        # print(new_model_dict)
        full_data["dubizzle"][make] = new_model_dict

    with open('car_data/cleaned_model_links.json', 'w') as f:
        json.dump(full_data, f, indent=2)