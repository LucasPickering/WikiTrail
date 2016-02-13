package me.lucaspickering.wikitrail;

import java.util.ArrayList;

/**
 * An {@code ArrayList} containing only strings. The only difference between this and {@code ArrayList<String>} is that
 * {@code contains} does not consider the case of letters when comparing strings
 */
public final class CaselessStringArrayList extends ArrayList<String> {

    @Override
    public boolean contains(Object o) {
        for (String s : this) {
            if (o == null) {
                if (s == null) {
                    return true;
                }
            } else if (o instanceof String && ((String) o).equalsIgnoreCase(s)) {
                return true;
            }
        }
        return false;
    }
}
