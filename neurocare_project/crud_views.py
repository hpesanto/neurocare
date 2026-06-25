import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _json_success(request, saved, row_template, item_context_name="item"):
    row_html = render_to_string(
        row_template, {item_context_name: saved}, request=request
    )
    return JsonResponse({"ok": True, "row_html": row_html, "id": str(saved.id)})


def _json_error(request, form, form_partial_template, title):
    form_html = render_to_string(
        form_partial_template,
        {"form": form, "title": title, "action": request.path},
        request=request,
    )
    return JsonResponse(
        {"ok": False, "form_html": form_html, "errors": form.errors.get_json_data()},
        status=400,
    )


def make_crud_views(
    *,
    model,
    form_class,
    list_template,
    row_template,
    form_template,
    form_partial_template,
    list_url_name,
    list_order_by,
    create_title,
    edit_title_fn,
    item_context_name="item",
    list_context_name="items",
    enable_delete=False,
):
    logger = logging.getLogger(model.__module__)

    @login_required
    def list_view(request):
        qs = model.objects.all().order_by(*list_order_by)
        form = form_class()
        return render(
            request, list_template, {list_context_name: list(qs), "form": form}
        )

    @login_required
    def create_view(request):
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                saved = form.save()
                if _is_ajax(request):
                    return _json_success(
                        request, saved, row_template, item_context_name
                    )
                return redirect(reverse(list_url_name))
            else:
                logger.warning(
                    "%s create form invalid: %s",
                    model.__name__,
                    form.errors.as_json(),
                )
                if _is_ajax(request):
                    return _json_error(
                        request, form, form_partial_template, create_title
                    )
        else:
            form = form_class()

        if _is_ajax(request):
            return render(
                request,
                form_partial_template,
                {"form": form, "title": create_title, "action": request.path},
            )

        return render(
            request,
            form_template,
            {"form": form, "title": create_title, "action": request.path},
        )

    @login_required
    def update_view(request, pk):
        instance = get_object_or_404(model, pk=pk)
        title = edit_title_fn(instance)
        if request.method == "POST":
            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                saved = form.save()
                if _is_ajax(request):
                    return _json_success(
                        request, saved, row_template, item_context_name
                    )
                return redirect(reverse(list_url_name))
            else:
                logger.warning(
                    "%s update form invalid (pk=%s): %s",
                    model.__name__,
                    pk,
                    form.errors.as_json(),
                )
                if _is_ajax(request):
                    return _json_error(request, form, form_partial_template, title)
        else:
            form = form_class(instance=instance)

        if _is_ajax(request):
            return render(
                request,
                form_partial_template,
                {
                    "form": form,
                    "title": title,
                    "instance": instance,
                    "action": request.path,
                },
            )

        return render(
            request,
            form_template,
            {"form": form, "title": title, "action": request.path},
        )

    views = {
        "list": list_view,
        "create": create_view,
        "update": update_view,
    }

    if enable_delete:

        @login_required
        def delete_view(request, pk):
            instance = get_object_or_404(model, pk=pk)
            if request.method == "POST":
                instance.delete()
                if _is_ajax(request):
                    return JsonResponse({"ok": True, "id": str(pk)})
                return redirect(reverse(list_url_name))
            if _is_ajax(request):
                return JsonResponse({"ok": False}, status=405)
            return redirect(reverse(list_url_name))

        views["delete"] = delete_view

    return views
