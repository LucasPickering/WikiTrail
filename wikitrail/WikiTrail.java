package wikitrail;

/**
 * Follows the wiki trail of a certain page to Philosophy. Inspired by the alt-text of http://xkcd.com/903.
 */
public class WikiTrail {

    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("No article specified. Specify the article name with arguments.\n" +
                    "Multi-word article names can be separated by either spaces or underscores.");
            return;
        }

        final StringBuilder articleNameBuilder = new StringBuilder();
        for (int i = 0; i < args.length; i++) {
            articleNameBuilder.append(args[i]);
            if (i < args.length - 1) {
                articleNameBuilder.append("_");
            }
        }
        String article = articleNameBuilder.toString();


    }
}
