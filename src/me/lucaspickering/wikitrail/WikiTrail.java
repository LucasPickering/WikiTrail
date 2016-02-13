package me.lucaspickering.wikitrail;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

/**
 * Follows the wiki trail of a certain page to Philosophy. Inspired by the alt-text of http://xkcd.com/903.
 */
public final class WikiTrail {

    private final CaselessStringArrayList trail = new CaselessStringArrayList();

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
            System.out.println("No article specified. Specify the article name with arguments.\n" +
                    "Multi-word article names can be separated by either spaces or underscores.");
        } else {
            String article = getArticleFromInput(args);
            while (true) {
                if (trail.contains(article)) {
                    System.out.println("Loop found! Here's the trail:");
                    break;
                }

                trail.add(article);
                if (article.equalsIgnoreCase("philosophy")) {
                    break;
                }

                try {
                    article = getNextArticle(article);
                } catch (IOException e) {
                    System.err.println("Error getting article \"" + article + "\"");
                    break;
                }
            }
            printTrail();
        }
    }

    /**
     * Get an article name from the given array of args. If there is more than one argument, they are appended together,
     * in order, and separated by underscores.
     *
     * @param args one or more arguments to append together (non-null, length > 0, does not contain null)
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
     * Gets the next article in the trail, from the given article. The next article is defined as the first article
     * linked in the given article's body that is not in parentheses or italics.
     *
     * @param article the first article
     * @return the next article
     */
    private String getNextArticle(String article) throws IOException {
        InputStream in = new URL("http://wikipedia.org/wiki/" + article).openStream();
        System.out.println(IOUtils.toString(in));
        IOUtils.closeQuietly(in);
        return "Philosophy";
    }

    /**
     * Print the current trail.
     */
    private void printTrail() {
        System.out.println(trail.size() + " article(s) traversed");
        for (int i = 0; i < trail.size(); i++) {
            System.out.println(i + 1 + ". " + trail.get(i).replace('_', ' '));
        }
    }
}
