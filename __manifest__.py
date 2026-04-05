{
    "name": "PawSafe",
    "summary": "Stray Animal Rescue ERP",
    "author": "PawSafe NGO",
    "depends": ["base"],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "views/shelter_views.xml",
        "views/rescuer_views.xml",
        "views/animal_views.xml",
        "views/rescue_case_views.xml",
        "views/vet_record_views.xml",
        "views/foster_views.xml",
        "views/adoption_views.xml",
        "views/menus.xml",
        "security/ir.model.access.csv",
    ]
}