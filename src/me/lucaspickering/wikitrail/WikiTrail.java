package me.lucaspickering.wikitrail;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
  private static final int FLAGS = Pattern.DOTALL;

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

        // Get the next article from Wikipedia. If an error occurred, break out.
        if ((article = getNextArticle(article)) == null) {
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
   * @return the next article, or {@code null} if an exception occurs
   */
  private String getNextArticle(String article) {
    InputStream in = null;
    String articleBody;
    try {
      in = new URL("https://en.wikipedia.org/wiki/" + article).openStream();
      articleBody = IOUtils.toString(in); // Get the string from the webpage
    } catch (IOException e) {
      // Error loading the article. Print a message and return null.
      System.err.printf("Error getting article \"%s\"\n", article);
      return null;
    } finally {
      // Close the stream, if it was opened
      if (in != null) {
        IOUtils.closeQuietly(in);
      }
    }
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
    final Pattern divContent = Pattern.compile("mw-body-content.*</div>", FLAGS);
    final Pattern pTag = Pattern.compile("<p>.*</p>", FLAGS);
    final Pattern aTag = Pattern.compile("<a href=\"/wiki/\\b[^>]*>(.*?)</a>", FLAGS);

    // Cut down to everything in the article body
    Matcher m = divContent.matcher(articleBody);
    if(m.find()) {
      // Cut down to everything in the outermost <p> tag
      m = pTag.matcher(m.group());
      if(m.find()) {
        // Get everything in an <a> tag
        m = aTag.matcher(m.group());
        while(m.find()) {
          System.out.println("--------------------------");
          System.out.println(m.group());
        }
      }
    } else {
      System.out.println("No match found");
    }
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
