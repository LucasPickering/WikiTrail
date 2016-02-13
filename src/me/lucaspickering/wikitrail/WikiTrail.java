package me.lucaspickering.wikitrail;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

/**
 * Follows the wiki trail of a certain page to Philosophy. A wiki trail is the series of pages you get
 * by starting at any page and continually following the first link in the main body of the article
 * that's not in italics or parentheses. The theory is that this will always lead to Philosophy.
 * Inspired by the alt-text of http://xkcd.com/903.
 */
public final class WikiTrail {

  /**
   * The (case-insensitive) article name that we're looking for. The program will stop when the trail
   * reaches the article by this name.
   */
  private static final String DESTINATION = "philosophy";

  private final CaselessStringLinkedList trail = new CaselessStringLinkedList();

  /* INVARIANTS
   *  - trail is non-null
   *  - All elements of trail are non-null
   */

  public static void main(String[] args) {
    new WikiTrail().run(args);
  }

  /**
   * Main loop of the program.
   *
   * @param args arguments passed from the command line
   */
  private void run(String... args) {
    if (args.length == 0) {
      // Print help text
      System.out.println("No article specified. Specify the article name with arguments.");
      System.out.println("Multi-word article names can be separated by spaces or underscores.");
    } else {
      String article = getArticleFromInput(args); // Get the article name from the args passed in
      System.out.println("Finding trail for: " + article); // Print the article name
      while (true) {
        // If article is already in the trail, terminate
        if (trail.contains(article)) {
          System.out.println("Loop found! Here's the trail:"); // printTrail() gets called below
          break;
        }

        trail.add(article); // Add article to the running trail
        // If we've reached the destination, we're done.
        if (article.equalsIgnoreCase(DESTINATION)) {
          break;
        }

        try {
          article = getNextArticle(article); // Get the next article from Wikipedia
        } catch (IOException e) {
          // Error getting the article
          System.err.println("Error getting article \"" + article + "\"");
          break;
        }
      }
      printTrail();
    }
  }

  /**
   * Get an article name from the given array of args. If there is more than one argument, they are
   * appended together, in order, and separated by underscores.
   *
   * @param args one or more arguments to append together (non-null, length > 0, does not contain
   *             null)
   * @return the appended article name
   */
  private String getArticleFromInput(String... args) {
    final StringBuilder articleNameBuilder = new StringBuilder();
    for (int i = 0; i < args.length; i++) {
      articleNameBuilder.append(args[i]);
      if (i < args.length - 1) {
        articleNameBuilder.append("_");
      }
    }
    return articleNameBuilder.toString();
  }

  /**
   * Gets the next article in the trail, from the given article. The next article is defined as the
   * first article linked in the given article's body that is not in parentheses or italics.
   *
   * @param article the first article
   * @return the next article
   * @throws IOException if an error occurs while retrieving the article
   */
  private String getNextArticle(String article) throws IOException {
    InputStream in = new URL("http://wikipedia.org/wiki/" + article).openStream();
    final String articleBody = IOUtils.toString(in); // Get the string from the webpage
    IOUtils.closeQuietly(in);
    return getNextArticleFromBody(articleBody);
  }

  /**
   * Gets the name of the first article linked in the given article body that abides by our rules of
   * the trail.
   *
   * @param articleBody the body of the article to be searched
   * @return the name of the first article validly linked in {@code articleBody}
   */
  private String getNextArticleFromBody(String articleBody) {
    // TODO: Filter out article name
    return "Philosophy";
  }

  /**
   * Print the current trail.
   */
  private void printTrail() {
    System.out.println(trail.size() + " article(s) traversed");
    int i = 1;
    for (String article : trail) {
      System.out.printf("%d. %s\n", i, article.replace('_', ' '));
      i++;
    }
  }
}
