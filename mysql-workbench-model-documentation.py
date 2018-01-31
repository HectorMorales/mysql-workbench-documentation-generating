# -*- encoding: utf-8 -*-
import os
import datetime
import webbrowser

from wb import *
import grt
import mforms as gui

ModuleInfo = DefineModule(name="Model Documentation",
                          author="Héctor Gregorio Morales Pacheco",
                          version="0.1.0")

@ModuleInfo.plugin("wb.util.generating_model_documentation",
                   caption="Generate HTML Documentation",
                   input=[wbinputs.currentCatalog()],
                   pluginMenu="Catalog")

@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def create_documentation(catalog):

    schema = catalog.defaultSchema
    tables = schema.tables

    sorted_tables = sorted(tables, key=lambda table: table.name)

    markup = get_header()
    markup = markup.replace("[PROJECTNAME]", schema.name)
    markup = markup.replace("[DESCRIPTION]", schema.comment)
    markup = markup.replace("[EDITION]", str(datetime.date.today()))

    markup += "<h2>Index</h2>\n"
    markup += "<ul>\n"
    for table in sorted_tables:
        markup += "<li><a href='#{0}'>{0}</a></li>\n".format(table.name)
    markup += "</ul>\n"

    for table in sorted_tables:
        markup += "<table id='{0}'>\n".format(table.name)
        markup += "<caption>{0}</caption>\n".format(table.name)
        markup += "<tr><td colspan='11'>{0}</td></tr>\n".format(table.comment)
        markup += get_colnames_columns()
        
        for column in table.columns:
            markup += "<tr>\n"
            markup += "    <td>{0}</td>\n".format(column.name)
            markup += "    <td>{0}</td>\n".format(column.formattedType)

            if table.isPrimaryKeyColumn(column):
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            if column.isNotNull == 1:
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            if False:
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            flags = list(column.flags)

            if flags.count("BINARY"):
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            if flags.count("UNSIGNED"):
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            if flags.count("ZEROFILL"):
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td>&nbsp;</td>\n"

            if column.autoIncrement == 1:
                markup += "    <td>&#10004;</td>\n"
            else:
                markup += "    <td class='attr'>&nbsp;</td>\n"

            markup += "    <td>{0}</td>\n".format(column.defaultValue)

            markup += "    <td>{0}</td>\n".format(column.comment)
            markup += "</tr>\n"

        markup += "</table>\n"
        
        if table.indices:
            markup += "<table id='{0}_indices'>\n".format(table.name)
            markup += get_colnames_indices()     
                        
            for index in table.indices:    
                markup += " <tr>\n"            
                markup += "    <td>{0}</td>\n".format(index.name)        
                markup += "    <td>{0}</td>\n".format(index.indexType)        
                markup += "    <td>"               
                markup += ", ".join(map(lambda x: x.referencedColumn.name, index.columns))
                markup += "    </td>\n"                               
                markup += "    <td>{0}</td>\n".format(index.comment)
                markup += " </tr>\n"
            
            markup += "</table>\n"

        if table.foreignKeys:
            markup += "<table id='{0}_foreignKeys'>\n".format(table.name)
            markup += get_colnames_foreignKeys()

            for foreignKey in table.foreignKeys:    
                            markup += " <tr>\n"            
                            markup += "    <td>{0}</td>\n".format(foreignKey.name)
                            markup += "    <td>"   
                            markup += ", ".join(map(lambda x: x.name, foreignKey.referencedColumns))                            
                            markup += "    </td>\n"                                       
                            markup += "    <td>"          
                            markup += ", ".join(set(map(lambda x: x.owner.name, foreignKey.referencedColumns)))                             
                            markup += "     </td>\n"                                 
                            markup += "     <td>{0}</td>\n".format(foreignKey.comment)
                            markup += " </tr>\n" 
           
            markup += "</table>\n"
  
    markup += get_footer()

    doc_path = os.path.dirname(grt.root.wb.docPath)

    dialog = gui.FileChooser(gui.SaveFile)
    dialog.set_title("Save HTML Documentation")
    dialog.set_directory(doc_path)
    response = dialog.run_modal()
    file_path = dialog.get_path()

    if response:
        try:
            html_file = open(file_path, "w")
        except IOError:
            text = "Could not open {0}.".format(file_path)
            gui.Utilities.show_error("Error saving the file", text, "Ok",
                                       "", "")
        else:
            html_file.write(markup)
            html_file.close()

            title = "{0} - Model Documentation".format(schema.name)
            text = "The Documentation was successfully generated."
            gui.Utilities.show_message(title, text, "Ok", "", "")

            try:
                webbrowser.open_new(file_path)
            except webbrowser.Error:
                print("Error: Could not open the Documentation in " +
                      "the Web browser.")
    
    return 0

def get_header():
    header = """<!DOCTYPE html>\n\
        <html>\n\
        <head>\n\
            <meta charset="UTF-8" />\n\
            <meta name="author" content="Model Documentation" />\n\
            <meta name="description" content="[PROJECTNAME] Model Documentation" />\n\
            <title>[PROJECTNAME] Model Documentation</title>\n\
            <style type="text/css">\n\
            table{\n\
                width: 100%;\n\
                margin-bottom: 30px;\n\
            }\n\
            abbr{\n\
                cursor: help;\n\
            }\n\
            table, td, th{\n\
                border-style: solid;\n\
                border-width: 1px;\n\
            }\n\
            table caption{\n\
                font-size: 120%;\n\
                font-weight: bold;\n\
            }\n\
            caption{\n\
                color: black;\n\
            }\n\
            td, th{\n\
                border-color: silver;\n\
            }\n\
            tr:hover{\n\
                color: #333;\n\
                background-color: #F2F2F2;\n\
            }\n\
            th{\n\
                background-color: silver;\n\
            }\n\
            td{\n\
                color: gray;\n\
            }\n\
            ul{\n\
                font-style: italic;\n\
            }\n\
            #title-sect{\n\
                color: gray;\n\
                text-align: right;\n\
            }\n\
            .proj-desc{\n\
                text-align: right;\n\
            }\n\
            </style>\n\
        </head>\n\
        <body>\n\
        <div id="title-sect">\n\
        <h1>[PROJECTNAME]</h1>\n\
        <h2>Model Documentation</h2>\n\
        <p>\n\
        <em>[EDITION]</em>\n\
        </p>\n\
        <p class="proj-desc">\n\
        <em>[DESCRIPTION]</em>\n\
        </p>\n\
        </div>\n\
    """
    return header


def get_colnames_columns():
    colnames = ("<tr>\n" +
                "    <th>Column</th>\n" +
                "    <th>DataType</th>\n" +
                "    <th><abbr title='Primary Key'>PK</abbr></th>\n" +
                "    <th><abbr title='Not Null'>NN</abbr></th>\n" +
                "    <th><abbr title='Unique'>UQ</abbr></th>\n" +
                "    <th><abbr title='Binary'>BIN</abbr></th>\n" +
                "    <th><abbr title='Unsigned'>UN</abbr></th>\n" +
                "    <th><abbr title='Zero Fill'>ZF</abbr></th>\n" +
                "    <th><abbr title='Auto Increment'>AI</abbr></th>\n" +
                "    <th>Default</th>\n" +
                "    <th>Comment</th>\n" +
                "</tr>\n")
    return colnames

def get_colnames_indices():
    colnames = ("<tr>\n" +
                "    <th>Index</th>\n" +
                "    <th>Type</th>\n" +
                "    <th>Columns</th>\n" +
                "    <th>Comment</th>\n" +
                "</tr>\n")
    return colnames

def get_colnames_foreignKeys():
    colnames = ("<tr>\n" +
                "    <th>Foreing Key</th>\n" +
                "    <th>Columns</th>\n" +
                "    <th>Referenced Table</th>\n" +
                "    <th>Comment</th>\n" +
                "</tr>\n")
    return colnames

def get_footer():
    return "</body>\n</html>"