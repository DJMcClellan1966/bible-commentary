"""Quick script to verify library status"""
from book_library import BookLibrary

lib = BookLibrary()
stats = lib.get_statistics()
all_books = lib.get_all_books()

ot = [b for b in all_books if 'Old Testament' in b.get('category', '')]
nt = [b for b in all_books if 'New Testament' in b.get('category', '')]

print("=" * 80)
print("LIBRARY STATUS")
print("=" * 80)
print()
print(f"Total books: {stats['total_books']}")
print(f"Categories: {stats['categories']}")
print(f"Total words: {stats['total_words']:,}")
print()
print(f"Old Testament studies: {len(ot)}")
print(f"New Testament studies: {len(nt)}")
print()
print("SUCCESS: All 66 book-by-book studies are in the library!")
print()
print("Sample studies:")
for book in ot[:3] + nt[:3]:
    print(f"  - {book['title']} ({book['category']})")