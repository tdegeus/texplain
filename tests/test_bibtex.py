import texplain


def test_bib():
    bib = {
        "foo": ["@article{foo,", "author = {b a},", "title = {b a},", "journal = {b a},", "}"],
        "bar": ["@article{bar,", "author = {a b},", "title = {a b},", "journal = {a b},", "}"],
    }

    bibfile = "\n\n".join(["\n".join(bib[key]) for key in ["foo", "bar"]])
    assert texplain.bib_select(bibfile, ["bar", "foo"]).strip() == bibfile.strip()

    bibfile = "\n\n".join(["\n".join(bib[key]) for key in ["foo", "bar"]])
    reduced = "\n\n".join(["\n".join(bib[key]) for key in ["bar"]])
    assert texplain.bib_select(bibfile, ["bar"]).strip() == reduced.strip()

    bibfile = "\n\n".join(["\n".join(bib[key]) for key in ["foo", "bar"]])
    reorder = "\n\n".join(["\n".join(bib[key]) for key in ["bar", "foo"]])
    assert texplain.bib_select(bibfile, ["bar", "foo"], reorder=True).strip() == reorder.strip()
