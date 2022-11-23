from string import Template
import yaml
from pathlib import Path

main_html_template = Template(
    """
    <!DOCTYPE html>
    <html class="no-js" lang="en">

    <head>
        $head
    </head>

    <body id="top">

        $preloader

        $header

        $content

        $footer

        $scripts

    </body>

</html>
    """
)


def generate_html(main_template: Template, kwargs: dict):
    """"""

    return main_template.substitute(
        head=generate_head(kwargs["page_title"]),
        preloader=generate_preloader(),
        header=generate_header(),
        content=kwargs["html_content_func"](**kwargs),
        footer=generate_footer(),
        scripts=generate_scripts(),
    )


def generate_head(page_title):

    return f"""
    <!--- basic page needs
    ================================================== -->
    <meta charset="utf-8">
    <title>{page_title} - deve ser aqui</title>
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- mobile specific metas
    ================================================== -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSS
    ================================================== -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/vendor.css">

    <!-- script
    ================================================== -->
    <script src="js/modernizr.js"></script>

    <!-- favicons
    ================================================== -->
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="manifest" href="site.webmanifest">
    """


def generate_preloader():
    return """
    <div id="preloader">
        <div id="loader"></div>
    </div>
    """


def generate_header():

    return """
    <header class="s-header">
        <div class="row s-header__content">
            <div class="s-header__logo">
                <a class="logo" href="index.html">
                    <img src="images/heart-svgrepo-com.svg" alt="Homepage">
                </a>
            </div>

            <nav class="s-header__nav-wrap">

                <h2 class="s-header__nav-heading h6">Site Navigation</h2>

                <ul class="s-header__nav">
                    <li><a href="donchan.html" title="">Home</a></li>
                    <li><a href="about.html" title="">Sobre</a></li>
                </ul> <!-- end header__nav -->

                <a href="#0" title="Close Menu" class="s-header__overlay-close close-mobile-menu">Close</a>

            </nav> <!-- end header__nav-wrap -->

            <a class="s-header__toggle-menu" href="#0" title="Menu"><span>Menu</span></a>


        </div> <!-- end s-header__content -->

    </header> <!-- end header -->
    
    """


def generate_about_content(**kwargs):

    main_img_path = kwargs.get("main_img_path")
    title = kwargs.get("post_title")
    text = kwargs.get("post_text")

    return f"""
    <section class="s-content">
        <div class="row">
            <div class="column large-12">

                <section>

                    <div class="s-content__media">
                        <img src="{main_img_path}" sizes="(max-width: 2100px) 100vw, 2100px" alt="">
                    </div> <!-- end s-content__media -->

                    <div class="s-content__primary">

                        <h1 class="s-content__title">{title}</h1>

                        {text}

                        <hr>
                    </div> <!-- end s-content__primary -->

                </section>

            </div> <!-- end column -->
        </div> <!-- end row -->
    </section> <!-- end s-content -->
    """


def generate_post_content(**kwargs):

    main_img_path = kwargs.get("main_img_path")
    title = kwargs.get("post_title")
    text = kwargs.get("post_text")
    date = kwargs.get("date")
    category = kwargs.get("category")

    return f"""
        <section class="s-content s-content--single">
        <div class="row">
            <div class="column large-12">

                <article class="s-post entry format-standard">

                    <div class="s-content__media">
                        <div class="s-content__post-thumb">
                            <img src="{main_img_path}" sizes="(max-width: 2100px) 100vw, 2100px" alt="">
                        </div>
                    </div> <!-- end s-content__media -->

                    <div class="s-content__primary">

                        <h2 class="s-content__title s-content__title--post">{title}</h2>

                        <ul class="s-content__post-meta">
                            <li class="date">{date}</li>
                            <li class="cat"><a href="">{category}</a></li>
                        </ul>

                        {text}

                    </div> <!-- end s-content__primary -->
                </article>

            </div> <!-- end column -->
        </div> <!-- end row -->
    </section> <!-- end s-content -->
    """


def generate_footer():

    return """
    <!-- footer
    ================================================== -->
    <footer class="s-footer">

        <div class="s-footer__bottom">
            <div class="row">
                <div class="column">
                    <div class="ss-copyright">
                        <span>Design by <a href="https://www.styleshout.com/">StyleShout</a></span>
                    </div> <!-- end ss-copyright -->
                </div>
            </div>

            <div class="ss-go-top">
                <a class="smoothscroll" title="Back to Top" href="#top">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M6 4h12v2H6zm5 10v6h2v-6h5l-6-6-6 6z" />
                    </svg>
                </a>
            </div> <!-- end ss-go-top -->
        </div> <!-- end s-footer__bottom -->

    </footer> <!-- end s-footer -->
    """


def generate_scripts():

    return """
    <!-- Java Script
    ================================================== -->
    <script src="js/jquery-3.2.1.min.js"></script>
    <script src="js/plugins.js"></script>
    <script src="js/main.js"></script>
    """


def generate_feed(main_template: Template, pages_dict: dict):

    feed_html = """"""

    for _, page_dict in pages_dict["posts"].items():
        print(page_dict)
        feed_html += generate_post_content(**page_dict)

    final_html = main_template.substitute(
        head=generate_head("Feed"),
        preloader=generate_preloader(),
        header=generate_header(),
        content=feed_html,
        footer=generate_footer(),
        scripts=generate_scripts(),
    )

    with open("index.html", "w") as f:
        f.write(final_html)


def generate_pages(main_template: Template, pages_dict: dict):

    # generate pages:

    for _, page_dict in pages_dict["pages"].items():
        html = generate_html(main_template, page_dict)

        with open(page_dict["path"], "w") as f:
            f.write(html)

    for _, page_dict in pages_dict["posts"].items():
        print(page_dict)
        html = generate_html(main_template, page_dict)

        with open(page_dict["path"], "w") as f:
            f.write(html)


if __name__ == "__main__":

    pages_dict = yaml.safe_load(Path("pages/main_pages.yaml").read_text())

    for key in pages_dict["pages"].keys():
        pages_dict["pages"][key]["html_content_func"] = generate_about_content

    for key in pages_dict["posts"].keys():
        pages_dict["posts"][key]["html_content_func"] = generate_post_content

    generate_pages(main_template=main_html_template, pages_dict=pages_dict)
    generate_feed(main_template=main_html_template, pages_dict=pages_dict)
