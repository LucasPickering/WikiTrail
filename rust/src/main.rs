use clap::Parser;
use scraper::{Html, Selector};
use std::fmt::Display;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(value_parser)]
    page_name: String,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct Article {
    name: String,
}

impl Article {
    fn new(name: String) -> Self {
        Self { name }
    }

    fn wiki_url(&self) -> String {
        format!("https://en.wikipedia.org/wiki/{}", self.name)
    }
}

struct Trail {
    articles: Vec<Article>,
}

impl Trail {
    fn new(initial_page: String) -> Self {
        let initial_article = Article::new(initial_page);
        Self {
            articles: vec![initial_article],
        }
    }

    fn resolve(&mut self) -> anyhow::Result<()> {
        loop {
            // Article list can't be empty, so unwrap is safe
            let last_article = self.articles.last().unwrap();
            let next_article = Self::load_next(last_article)?;

            // Check terminal conditions. This cycle check is O(n^2), but our
            // chain size is going to be so small that it's not worth keeping
            // a hash set around as well to make it O(n)
            let is_end = next_article.name == "Philosophy";
            let is_dupe = self.articles.contains(&next_article);
            // Add the article *before* breaking, so it shoulds up in the output
            self.articles.push(next_article);
            if is_end || is_dupe {
                break;
            }
        }
        Ok(())
    }

    fn load_next(article: &Article) -> anyhow::Result<Article> {
        let body = reqwest::blocking::get(article.wiki_url())?.text()?;
        // TODO check response code
        let document = Html::parse_document(&body);
        let selector = Selector::parse("p a").unwrap();
        Ok(Article::new("Philosophy".into()))
    }
}

impl Display for Trail {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for article in &self.articles {
            writeln!(f, "- {}", article.name)?;
        }
        Ok(())
    }
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    let mut trail = Trail::new(args.page_name);
    trail.resolve()?;
    println!("{}", trail);
    Ok(())
}
