from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from CFT.forms import NoteForm
from .models import Note


@login_required()
def index(request):
    creator = request.user.pk
    creator_notes = Note.objects.filter(creator=creator)[::-1]

    if request.method == 'POST':
        fulltext_search = request.POST.get('anything')
        if fulltext_search:
            search_date = Note.objects.filter(
                Q(title__icontains=fulltext_search) |
                Q(note__icontains=fulltext_search) |
                Q(created__icontains=fulltext_search.format('Y-m-d'))
            )

            return render(request, 'search.html', {'search_date': search_date})

    return render(request, 'index.html', {'creator_notes': creator_notes})


# функция добавления заметки
@login_required()
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            # сохранение формы
            post = form.save(commit=False)
            # привязка юзера к заметке
            post.creator = request.user
            post.save()
            # перенаправление на главную
            return redirect('index')
    else:
        form = NoteForm()

    return render(request, 'add_note.html', {'form': form})


@login_required()
def edit(request, pk):
    note = Note.objects.get(pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm(instance=note)

    return render(request, 'edit.html', {'form': form, 'note': note})


@login_required()
def delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    messages.success(request, 'Заметка успешно удалена')
    return redirect('index')


# функция регистрации
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # сохранение формы
            form.save()
            # автоматическая аутентификация пользователя
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            # создание первой заметки пользователю
            new_note = Note.objects.create(
                title='Ваша первая заметка',
                note='Здесь вы можете писать все что захотите',
                creator=request.user
            )
            # перенаправление на главную
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/registration.html', {'form': form})
