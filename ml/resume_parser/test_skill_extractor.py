import unittest

from skill_extractor import (
    SKILL_ONTOLOGY,
    normalize_skill,
    extract_skills_from_text,
    skill_in_text,
    normalize_text,
)


def flat_all_skills(text):
    """Helper: run full extraction and flatten to a set of canonical names."""
    result = extract_skills_from_text(text)
    flat = set()
    for skills in result.values():
        flat.update(skills)
    return flat


class TestExistingSkillsStillWork(unittest.TestCase):
    """Skills that were already supported before this update."""

    def test_core_languages(self):
        found = flat_all_skills("Python, Java, C, C++, C#, JavaScript, TypeScript, SQL")
        for s in ["Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "SQL"]:
            self.assertIn(s, found)

    def test_web_frameworks_unchanged(self):
        found = flat_all_skills("React.js, Node.js, Django, Vue.js, Tailwind CSS")
        for s in ["React", "Node.js", "Django", "Vue.js", "Tailwind CSS"]:
            self.assertIn(s, found)

    def test_java_vs_javascript_not_confused(self):
        found = flat_all_skills("I know JavaScript well.")
        self.assertIn("JavaScript", found)
        self.assertNotIn("Java", found)

    def test_ai_ml_existing(self):
        found = flat_all_skills("Machine Learning, Deep Learning, TensorFlow, PyTorch")
        for s in ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"]:
            self.assertIn(s, found)


class TestNewlyAddedSkills(unittest.TestCase):
    """Spot-check newly added skills across every new/extended category."""

    def test_dotnet_family(self):
        found = flat_all_skills("Experience with .NET and .NET Core applications")
        self.assertIn(".NET", found)
        self.assertIn(".NET Core", found)

    def test_web_frameworks_additions(self):
        found = flat_all_skills("Bootstrap, CSS3, HTML5, jQuery, Microsoft IIS")
        for s in ["Bootstrap", "CSS", "HTML", "jQuery", "Microsoft IIS"]:
            self.assertIn(s, found)

    def test_devops_new_category(self):
        found = flat_all_skills("Ansible, Chef, Puppet, Terraform, Jenkins, GitLab CI, CI/CD")
        for s in ["Ansible", "Chef", "Puppet", "Terraform", "Jenkins", "GitLab CI", "CI/CD"]:
            self.assertIn(s, found)

    def test_data_engineering_new_category(self):
        found = flat_all_skills("Big Data processing with Apache Spark")
        self.assertIn("Big Data", found)
        self.assertIn("Apache Spark", found)

    def test_bare_spark_not_matched(self):
        # CSV explicitly flagged bare "Spark" as ambiguous - only the
        # unambiguous "Apache Spark" phrase should match.
        found = flat_all_skills("The team named their mascot Spark.")
        self.assertNotIn("Apache Spark", found)

    def test_networking_new_category(self):
        found = flat_all_skills("Configured DNS, HTTP, NTP and TCP/IP settings")
        for s in ["DNS", "HTTP", "NTP", "TCP/IP"]:
            self.assertIn(s, found)

    def test_testing_new_category(self):
        found = flat_all_skills(
            "Selenium, Jasmine, Karma, PyUnit, Protractor, Regression Testing, Exploratory Testing"
        )
        for s in [
            "Selenium",
            "Jasmine",
            "Karma",
            "PyUnit",
            "Protractor",
            "Regression Testing",
            "Exploratory Testing",
        ]:
            self.assertIn(s, found)

    def test_mobile_development_new_category(self):
        found = flat_all_skills("Cocoa Touch, Core Data, Core Animation, Core Graphics, Core Text, Ionic, PhoneGap")
        for s in [
            "Cocoa Touch",
            "Core Data",
            "Core Animation",
            "Core Graphics",
            "Core Text",
            "Ionic",
            "PhoneGap",
        ]:
            self.assertIn(s, found)

    def test_operating_systems_new_category(self):
        found = flat_all_skills("Comfortable with both Linux and Windows environments")
        self.assertIn("Linux", found)
        self.assertIn("Windows", found)

    def test_cybersecurity_new_category(self):
        found = flat_all_skills("Administered OpenAM for identity management")
        self.assertIn("OpenAM", found)

    def test_other_new_category(self):
        found = flat_all_skills("Built on Mule, integrated SYSPRO ERP, deployed via WordPress")
        for s in ["Mule (MuleSoft)", "SYSPRO ERP", "WordPress"]:
            self.assertIn(s, found)

    def test_databases_additions(self):
        found = flat_all_skills(
            "Database Design, Database Administration, Elasticsearch, Microsoft SQL Server, Relational Database Design"
        )
        for s in [
            "Database Design",
            "Database Administration",
            "Elasticsearch",
            "Microsoft SQL Server",
            "Relational Database Design",
        ]:
            self.assertIn(s, found)

    def test_ai_ml_additions(self):
        found = flat_all_skills("Artificial Neural Network (ANN), Image Processing, Keras, OpenCV")
        for s in ["Artificial Neural Networks (ANN)", "Image Processing", "Keras", "OpenCV"]:
            self.assertIn(s, found)

    def test_cloud_additions(self):
        found = flat_all_skills("Azure Functions, Cloud Computing, Cloudify")
        for s in ["Azure Functions", "Cloud Computing", "Cloudify"]:
            self.assertIn(s, found)

    def test_developer_tools_additions(self):
        found = flat_all_skills("Bash, Gerrit, IBM Rational Clearcase, Version Control")
        for s in ["Bash", "Gerrit", "IBM Rational ClearCase", "Version Control"]:
            self.assertIn(s, found)

    def test_software_engineering_additions(self):
        found = flat_all_skills("Microservices pattern, Object-oriented design")
        self.assertIn("Microservices", found)
        self.assertIn("Object-Oriented Design", found)

    def test_graphql(self):
        found = flat_all_skills("Built RESTful APIs and GraphQL endpoints")
        self.assertIn("GraphQL", found)
        self.assertIn("REST API", found)

    def test_bare_rest_not_matched(self):
        # Bare "REST" was deliberately excluded as an alias for REST API -
        # it's an ordinary English word ("take a rest") and would produce
        # too many false positives. Only "rest api"/"restful ..." match.
        found = flat_all_skills("Please rest before the interview.")
        self.assertNotIn("REST API", found)

    def test_programming_language_additions(self):
        found = flat_all_skills("Objective-C, Perl, Scala")
        for s in ["Objective-C", "Perl", "Scala"]:
            self.assertIn(s, found)


class TestAliasesAndNormalization(unittest.TestCase):
    def test_angular_8x_alias(self):
        self.assertEqual(normalize_skill("Angular 8.x+"), "Angular")

    def test_oracle_database_alias(self):
        self.assertEqual(normalize_skill("Oracle Database"), "Oracle")

    def test_restful_services_alias(self):
        self.assertEqual(normalize_skill("Restful services"), "REST API")

    def test_mssql_alias(self):
        self.assertEqual(normalize_skill("MsSQL"), "Microsoft SQL Server")


class TestConfusingPairs(unittest.TestCase):
    def test_c_and_cpp_both_distinct_entries_exist(self):
        self.assertIn("C", SKILL_ONTOLOGY["programming_languages"])
        self.assertIn("C++", SKILL_ONTOLOGY["programming_languages"])
        self.assertNotEqual(
            SKILL_ONTOLOGY["programming_languages"]["C"],
            SKILL_ONTOLOGY["programming_languages"]["C++"],
        )

    def test_dotnet_and_dotnet_core_both_distinct_entries_exist(self):
        self.assertIn(".NET", SKILL_ONTOLOGY["web_frameworks"])
        self.assertIn(".NET Core", SKILL_ONTOLOGY["web_frameworks"])

    def test_cpp_does_not_also_extract_c(self):
        found = flat_all_skills("Experienced in C++ development")
        self.assertIn("C++", found)
        self.assertNotIn("C", found)

    def test_csharp_does_not_also_extract_c(self):
        found = flat_all_skills("Experienced in C# development")
        self.assertIn("C#", found)
        self.assertNotIn("C", found)

    def test_dotnet_core_does_not_also_extract_dotnet(self):
        found = flat_all_skills("Built applications using .NET Core")
        self.assertIn(".NET Core", found)
        self.assertNotIn(".NET", found)

    def test_independent_c_and_cpp_mentions_are_both_extracted(self):
        found = flat_all_skills("Experience with C and C++")
        self.assertIn("C", found)
        self.assertIn("C++", found)

    def test_relational_database_design_suppresses_shorter_phrase(self):
        found = flat_all_skills("Relational Database Design")
        self.assertIn("Relational Database Design", found)
        self.assertNotIn("Database Design", found)

    def test_java_javascript_distinct(self):
        text = normalize_text("Java and JavaScript are different languages")
        self.assertTrue(skill_in_text(text, "java"))
        self.assertTrue(skill_in_text(text, "javascript"))
        # "java" alone should not match inside "javascript"
        self.assertFalse(skill_in_text(normalize_text("javascript"), "java"))


class TestPunctuationSensitiveMatching(unittest.TestCase):
    def test_dotnet_punctuation(self):
        self.assertTrue(skill_in_text(normalize_text("skills: .NET, C#"), ".net"))

    def test_csharp_punctuation(self):
        self.assertTrue(skill_in_text(normalize_text("skills: .NET, C#"), "c#"))

    def test_cpp_punctuation(self):
        self.assertTrue(skill_in_text(normalize_text("Proficient in C++"), "c++"))

    def test_cicd_punctuation(self):
        self.assertTrue(skill_in_text(normalize_text("Built CI/CD pipelines"), "ci/cd"))

    def test_tcpip_punctuation(self):
        self.assertTrue(skill_in_text(normalize_text("Deep knowledge of TCP/IP"), "tcp/ip"))

    def test_http_does_not_match_https(self):
        # boundary check: "http" alias should not match inside "https"
        self.assertFalse(skill_in_text(normalize_text("Uses HTTPS everywhere"), "http"))


class TestDuplicatePrevention(unittest.TestCase):
    def test_repeated_mentions_not_duplicated(self):
        result = extract_skills_from_text("Python Python Python, python developer, PYTHON")
        self.assertEqual(result["programming_languages"].count("Python"), 1)

    def test_no_duplicate_canonical_across_aliases(self):
        # "react", "react.js", "reactjs" are all aliases of the same skill
        result = extract_skills_from_text("react react.js reactjs")
        self.assertEqual(result["web_frameworks"].count("React"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
