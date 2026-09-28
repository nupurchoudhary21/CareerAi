from resume_parser.skill_extractor import extract_skills_from_text


def test_new_skills():
    text = """
    Experience with Flutter development.
    Knowledge of database administration.
    Experience with Active Directory and FTP.
    Familiarity with manual testing and integration testing.
    """

    skills = extract_skills_from_text(text)

    expected_skills = [
        "Flutter",
        "Database Administration",
        "Active Directory",
        "FTP",
        "Manual Testing",
        "Integration Testing",
    ]

    for skill in expected_skills:
        assert skill in skills, f"{skill} was not detected"


def test_unrelated_text():
    text = "I enjoy reading books and listening to music."

    skills = extract_skills_from_text(text)

    assert skills == []