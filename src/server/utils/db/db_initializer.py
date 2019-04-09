from tools import db_utils


def init_applications_table():
    db_utils.exec_command("DROP TABLE applications")
    db_utils.exec_command(
        "CREATE TABLE applications (id serial not null primary key, name text, developer text, category name, "
        "dev_url text , pp_url text, is_new boolean DEFAULT true )")


def init_pp_tables():
    db_utils.exec_command("DROP TABLE privacy_policy")
    db_utils.exec_command("DROP TABLE privacy_policy_paragraphs")
    db_utils.exec_command("CREATE TABLE privacy_policy (id serial not null primary key, \
                                                        application_id numeric, pp_url text, html text, clean_html text,\
                                                        process_status text, process_status_details text, url_return_code numeric, url_return_value text)")
    db_utils.exec_command("CREATE TABLE privacy_policy_paragraphs (id serial not null primary key, \
                                                                   pp_url text, paragraph text, index numeric,privacy_policy_id numeric)")


def init_paragraphs_prediction_tables():
    db_utils.exec_command("DROP TABLE privacy_policy_paragraphs_prediction")
    db_utils.exec_command("CREATE TABLE privacy_policy_paragraphs_prediction (id serial not null primary key, \
                                                        running_id numeric,topic_id numeric, probability numeric, paragraph text)")


def init_db():
    init_applications_table()
    init_pp_tables()
    init_paragraphs_prediction_tables()


if __name__ == '__main__':
    init_db()
