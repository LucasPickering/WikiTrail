package me.lucaspickering.wikitrail;

import java.util.LinkedList;

/**
 * An {@link LinkedList} containing only strings. The only difference between this and {@code
 * LinkedList<String>} is that {@link #contains} does not consider the case of letters when comparing
 * strings.
 */
public final class CaselessStringLinkedList extends LinkedList<String> {

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
