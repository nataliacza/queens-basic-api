""" This in-memory 'database' is hardcoded due to impermanent state of items on Deta Cloud. """

from uuid import UUID

queen_db = {
    UUID("d43ee99a-038e-4381-8b10-b014ff7253cd"): {
        "queen_id": UUID("d43ee99a-038e-4381-8b10-b014ff7253cd"),
        "nickname": "Hrabina",
        "status": "Active",
        "info": None,
        "on_stage_since": None,
        "hometown": None,
        "residence": None,
        "email": "TheCountessDQ@gmail.com",
        "web": None,
        "instagram": "https://www.instagram.com/hrabina.drag/",
        "facebook": "https://www.facebook.com/CountesRose/",
        "twitter": None,
        "tags": [
            {"category_id": UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf"),
             "name": "wig"},
            {"category_id": UUID("8898ea70-2c02-4551-9658-691e3293c516"),
             "name": "glam"}
        ]
    },
    UUID("6c9463b7-bf69-4f8d-87dd-f1aa10a27762"): {
        "queen_id": UUID("6c9463b7-bf69-4f8d-87dd-f1aa10a27762"),
        "nickname": "Misia Joachim",
        "status": "Active",
        "info": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut...",
        "on_stage_since": 2011,
        "hometown": None,
        "residence": None,
        "email": "joachimmakeup@gmail.com",
        "web": None,
        "instagram": "https://www.instagram.com/misiajoachim/",
        "facebook": "https://www.facebook.com/profile.php?id=100071518396045",
        "twitter": None,
        "tags": [
            {"category_id": UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2"),
             "name": "makeup"},
            {"category_id": UUID("8898ea70-2c02-4551-9658-691e3293c516"),
             "name": "glam"}
        ]
    },
    UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"): {
        "queen_id": UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"),
        "nickname": "Twoja Stara",
        "status": "Active",
        "info": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut...",
        "on_stage_since": 2000,
        "hometown": {
            "city_id": UUID("eb195501-603e-46f4-b3f1-71f7de304a28"),
            "name": "Warszawa",
            "region": "Mazowieckie",
            "country": "Polska"},
        "residence": {
            "city_id": UUID("eb195501-603e-46f4-b3f1-71f7de304a28"),
            "name": "Warszawa",
            "region": "Mazowieckie",
            "country": "Polska"},
        "email": "twoja@stara.pl",
        "web": "https://www.twoja-stara.com",
        "instagram": "https://www.instagram.com/twoja___stara/",
        "facebook": "https://www.facebook.com/TwojaStaraDQ/",
        "twitter": "https://www.twitter.com/twoja-stara/",
        "tags": [
            {"category_id": UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35"),
             "name": "camp"}
        ]
    }
}

category_db = {
    UUID("8898ea70-2c02-4551-9658-691e3293c516"): {
        "category_id": UUID("8898ea70-2c02-4551-9658-691e3293c516"),
        "name": "glam"
    },
    UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2"): {
        "category_id": UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2"),
        "name": "makeup"
    },
    UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35"): {
        "category_id": UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35"),
        "name": "camp"
    },
    UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf"): {
        "category_id": UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf"),
        "name": "wig"
    }
}

city_db = {
    UUID("eb195501-603e-46f4-b3f1-71f7de304a28"): {
        "city_id": UUID("eb195501-603e-46f4-b3f1-71f7de304a28"),
        "name": "Warszawa",
        "region": "Mazowieckie",
        "country": "Polska"
    },
    UUID("7ced7771-64ff-44e5-8a87-c0f4126a6328"): {
        "city_id": UUID("7ced7771-64ff-44e5-8a87-c0f4126a6328"),
        "name": "Kraków",
        "region": "Małopolskie",
        "country": "Polska"
    }
}
