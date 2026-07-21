from app.schemes.post_scheme import Post_Create, Post_Update


# 실제 데이터베이스 대신 게시글을 저장할 리스트입니다.
post_list = []

# 새 게시글에 부여할 번호입니다.
post_id = 1


def create_post(post: Post_Create) -> dict:
    """새 게시글을 생성합니다."""
    global post_id

    new_post = {
        "post_id": post_id,
        "user_id": post.user_id,
        "title": post.title,
        "content": post.content,
    }

    post_list.append(new_post)
    post_id = post_id + 1

    return new_post


def get_posts() -> list[dict]:
    """저장된 모든 게시글을 반환합니다."""
    return post_list


def get_post(post_id: int) -> dict | None:
    """게시글 번호와 일치하는 게시글 하나를 찾습니다."""
    for post in post_list:
        if post["post_id"] == post_id:
            return post

    return None


def update_post(post_id: int, update_data: Post_Update) -> dict | None:
    """게시글 번호와 일치하는 게시글을 수정합니다."""
    post = get_post(post_id)

    if post is None:
        return None

    post["title"] = update_data.title
    post["content"] = update_data.content

    return post


def delete_post(post_id: int) -> dict | None:
    """게시글 번호와 일치하는 게시글을 삭제합니다."""
    post = get_post(post_id)

    if post is None:
        return None

    post_list.remove(post)
    return post
