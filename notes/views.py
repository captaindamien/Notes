from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from CFT.forms import NoteForm
from .models import Note


# функция главной страницы (отображение таблицы с заметками из бд)
@login_required()
def index(request):
    # получения текущего пользователя
    creator = request.user.pk
    # получение заметок пользователя
    creator_notes = Note.objects.filter(creator=creator)[::-1]

    # кол-во отображаемых записей на 1 страницу
    paginator = Paginator(creator_notes, 7)
    # получение текущей страницы
    page_number = request.GET.get('page')
    # объект пагинации
    page_object = paginator.get_page(page_number)
    # передача данных из бд + пагинация на главную
    return render(request, 'index.html', {'page_object': page_object})


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


# функция редактирования
@login_required()
def edit(request, pk):
    note = Note.objects.get(pk=pk)

    if request.method == 'POST':
        # передача данных из формы в модель
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            # перенаправление на главную
            return redirect('index')
    else:
        # передача данных из модели в форму
        form = NoteForm(instance=note)
    # рендер страницы изменения заметки
    return render(request, 'edit.html', {'form': form, 'note': note})


# функция удаления
@login_required()
def delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    # сообщение об успешном удалении
    messages.success(request, 'Заметка успешно удалена')
    # перенаправление на главную
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
        # рендер пустой формы
        form = UserCreationForm()

    return render(request, 'registration/registration.html', {'form': form})
