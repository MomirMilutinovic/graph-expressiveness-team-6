from html_datasource.implementation import HtmlDataSource


if __name__ == '__main__':
    # Create an instance of the HTML data source
    src = "https://guthib.com"
    html_data_source = HtmlDataSource()

    # Get the data from the HTML page
    gg = html_data_source.provide(url=src)
    found_element = next(filter(lambda x: x.data["tag"] == "html", gg.nodes), None)
