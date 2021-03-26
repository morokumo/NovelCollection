from enum import Enum


class SQL:
    # CREATE TABLE
    create_table_novel_information = '''
                create table if not exists novel_information(
                        novel_code VARCHAR (32) NOT NULL ,
                        site_genre INTEGER NOT NULL ,
                        
                        title VARCHAR (1024) NOT NULL ,
                        user_id INTEGER NOT NULL ,
                        writer VARCHAR (256) NOT NULL ,
                        story TEXT NOT NULL ,
                        
                        category VARCHAR (128),
                        genre VARCHAR (128),      
                        
                        novel_type BOOLEAN NOT NULL ,
                        is_end BOOLEAN NOT NULL ,
                        
                        first_upload_date timestamp NOT NULL ,
                        last_upload_date timestamp NOT NULL ,
                        
                        number_of_episode INTEGER NOT NULL ,
                        number_of_character INTEGER NOT NULL ,
                        
                        favorite_cnt INTEGER ,
                        review_cnt INTEGER ,
                        evaluation_point INTEGER ,
                        number_of_evaluator INTEGER,
                        r_18 BOOLEAN NOT NULL ,
                        PRIMARY KEY (novel_code,site_genre)
                );
    '''

    create_table_novel_content = '''
                create table if not exists novel_content(
                    novel_code varchar(32),
                    site_genre INTEGER ,
                    episode INTEGER ,
                    title VARCHAR (1024),
                    body TEXT,
                    PRIMARY KEY (novel_code, site_genre,episode),
                    FOREIGN KEY (novel_code, site_genre) REFERENCES novel_information (novel_code, site_genre)  
                );
    
    '''

    create_table_novel_tag = '''
                create table if not exists novel_tag(
                    id INTEGER,
                    tag_name VARCHAR (256) ,
                    novel_code VARCHAR (32) ,
                    site_genre INTEGER,
                    PRIMARY KEY (id),
                    FOREIGN KEY (novel_code, site_genre) REFERENCES novel_information (novel_code, site_genre) 
                );
    
    '''

    # INSERT
    insert_novel_information = '''
                insert into novel_information
                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''

    insert_novel_content = '''
                insert into novel_content
                values(?,?,?,?,?)
    '''

    insert_novel_tag = '''
                insert into novel_tag (tag_name,novel_code,site_genre)
                values(?,?,?)
    '''
    # update
    update_novel_information = '''
                update novel_information set
                title = ? ,
                writer = ? ,
                story = ? ,
                is_end = ?,
                last_upload_date = ?,
                number_of_episode = ?,
                number_of_character = ?,
                favorite_cnt = ?,
                review_cnt = ?,
                evaluation_point = ?,
                number_of_evaluator = ?,
                where
                novel_code = ? and site_genre = ?;
    '''

    update_novel_content = '''
                update novel_content set
                episode = ? ,
                title = ?,
                body = ?,
                where
                novel_code = ? and site_genre = ?;
    '''

    # SELECT
    find_novel_information = '''
            SELECT * FROM NOVEL_INFORMATION
    '''

    find_novel_content = '''
            SELECT * FROM NOVEL_CONTENT
    '''


    find_novel_tag = '''
            SELECT * FROM NOVEL_TAG
    '''